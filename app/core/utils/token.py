import os
import datetime

import jwt

ExpiredSignatureError = jwt.ExpiredSignatureError
InvalidTokenError = jwt.InvalidTokenError


def encode_token(data,
                 algorithm='HS256',
                 time_delta=datetime.timedelta(minutes=10)):
    """
        Encoding the given data to JWT token
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + time_delta,
            'iat': datetime.datetime.utcnow(),
            'data': data
        }

        return jwt.encode(
            payload,
            os.environ.get("JWT_SECRET_KEY", "very_secret_jwt"),
            algorithm=algorithm
        ).decode('utf-8')

    except Exception as e:
        return e


def decode_token(token):
    """
        Decoding the encoded data given the token
    """
    payload = jwt.decode(
        token,
        os.environ.get("JWT_SECRET_KEY", "very_secret_jwt")
    )
    return payload.get('data')
