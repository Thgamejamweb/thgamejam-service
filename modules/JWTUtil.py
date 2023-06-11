import base64
import datetime
from typing import Any

import jwt


def generateKey(secretKey: str) -> bytes:
    if len(secretKey) < 32:
        return base64.b64encode(secretKey.ljust(32, '0').encode('utf-8'))
    return base64.b64encode(secretKey.encode('utf-8'))


def generateToken(secret_key: str, data: Any, date: datetime.datetime) -> str:
    token = jwt.encode(
        {"user": data, "exp": date},
        secret_key,
        algorithm="HS256"
    )
    return token


def parserToken(secret_key: str, token: str) -> str:
    decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
    return decoded_token["user"]
