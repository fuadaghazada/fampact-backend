import rollbar
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

# from core.models import PushToken


class ExpoNotification(object):
    """
        Utility class for handling sending Notification to Expo client
        devices
    """

    @staticmethod
    def send(token, message, extra=None):
        try:
            response = PushClient().publish(
                PushMessage(to=token,
                            body=message,
                            data=extra))
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'errors': exc.errors,
                    'response_data': exc.response_data,
                })
            raise
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra
                })
            raise exc

        try:
            # We got a response back, but we don't know
            # whether it's an error yet.
            # This call raises errors so
            # we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            # PushToken.objects.filter(token=token).update(active=False)
            pass

        except PushResponseError as exc:
            # Encountered some other per-notification error.
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'push_response': exc.push_response._asdict(),
                })
            raise exc
