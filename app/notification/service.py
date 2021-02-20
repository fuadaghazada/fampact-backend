import json

from uuid import uuid4
from core.utils import cache, timezone

from .options.constants import USER_CHANNEL_KEY, USER_NOTIFICATIONS
from .tasks import send_notification, populate_data


class Notification(object):
    """Notification services"""

    @staticmethod
    def send(user_id, message, data, data_type):
        channel_name = cache.get_key(
            pre_key=USER_CHANNEL_KEY,
            key=user_id
        )
        notification_id = str(uuid4().hex)
        timestamp = str(timezone.now().timestamp())

        send_notification.delay(
            channel_name,
            notification_id,
            message,
            data,
            data_type,
            timestamp
        )

        cache.h_set(
            pre_name=USER_NOTIFICATIONS,
            name=user_id,
            key=notification_id,
            value=json.dumps({
                'message': message,
                'data': data,
                'data_type': data_type,
                'read': False,
                'timestamp': timestamp
            })
        )

    @staticmethod
    def get_notifications(user_id):
        raw = cache.h_get_all(
            pre_name=USER_NOTIFICATIONS,
            name=user_id
        )
        notifications = []
        for n_key in raw.keys():
            data = json.loads(raw.get(n_key))

            if data['read'] is False:
                data['id'] = n_key
                notifications.append(data)

        return notifications

    @staticmethod
    def read_notification(user_id, notification_id):
        raw = cache.h_get(
            pre_name=USER_NOTIFICATIONS,
            name=user_id,
            key=notification_id
        )
        data = json.loads(raw)
        data['read'] = True

        cache.h_set(
            pre_name=USER_NOTIFICATIONS,
            name=user_id,
            key=notification_id,
            value=json.dumps(data)
        )

    @staticmethod
    def populate(data_type, data):
        """Populates the given data to all channels connected"""
        timestamp = str(timezone.now().timestamp())

        populate_data.delay(data_type, data, timestamp)
