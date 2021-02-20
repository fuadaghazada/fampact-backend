from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from app.celery import app
from .options.constants import GLOBAL_CHANNEL_NAME

channel_layer = get_channel_layer()


@app.task
def send_notification(
        channel_name,
        notification_id,
        message, data,
        data_type,
        timestamp
):
    if channel_name:
        async_to_sync(channel_layer.send)(channel_name, {
            'type': 'send_data',
            'notification_id': notification_id,
            'message': message,
            'data': data,
            'data_type': data_type,
            'read': False,
            'timestamp': timestamp,
            'global': False
        })

        return f'Notification sent to Channel: {channel_name}'


@app.task
def populate_data(data_type, data, timestamp):
    async_to_sync(channel_layer.group_send)(GLOBAL_CHANNEL_NAME, {
        'type': 'send_data',
        'notification_id': None,
        'message': None,
        'data': data,
        'data_type': data_type,
        'read': None,
        'timestamp': timestamp,
        'global': True
    })

    return f'Population: "{GLOBAL_CHANNEL_NAME}"'
