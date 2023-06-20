import datetime
from dataclasses import asdict
from typing import Any, Type

import jwt


def generateToken(secret_key: str, data: Any, expiration_time: int) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
    token = jwt.encode(
        {"user": data.__dict__(), "exp": expiration},
        secret_key,
        algorithm="HS256"
    )
    return token


def parserToken(secret_key: str, token: str, data: Type[Any]) -> dict:
    decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_exp": True})
    return decoded_token["user"]
