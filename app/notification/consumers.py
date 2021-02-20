from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from core.utils import cache
from .service import Notification
from .options.constants import USER_CHANNEL_KEY, GLOBAL_CHANNEL_NAME


class NotificationConsumer(JsonWebsocketConsumer):
    """
        Notification consumer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def connect(self):
        user = self.scope['user']
        print(f"{user} connected!")

        cache.set_key(
            pre_key=USER_CHANNEL_KEY,
            key=user.id,
            value=self.channel_name
        )

        # Adding the channel name to global channels group
        async_to_sync(self.channel_layer.group_add)(
            GLOBAL_CHANNEL_NAME,
            self.channel_name
        )

        self.accept()
        self.user = user

        self.get_notifications()

    def disconnect(self, code):
        print(f"{self.user} disconnected!")

        cache.remove_key(pre_key=USER_CHANNEL_KEY, key=self.user.id)

        self.close()

    def send_data(self, event):
        self.send_json(event)

    def get_notifications(self):
        self.send_data({
            'type': 'get_notifications',
            'notifications': Notification.get_notifications(self.user.id)
        })

    def receive_json(self, content, **kwargs):
        notification_type = content and content.get('notification_type')
        if not notification_type:
            return

        # Read notification
        if notification_type == 'read_notification':
            user = self.scope['user']
            notification_id = content.get('notification_id')

            Notification.read_notification(user.id, notification_id)
            self.get_notifications()
