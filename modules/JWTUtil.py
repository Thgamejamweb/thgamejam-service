import datetime
from typing import Any, Type

import jwt


def generateToken(secret_key: str, data: Any, date: datetime.datetime, expiration_time: int) -> str:
    expiration_date = date + datetime.timedelta(seconds=expiration_time)
    token = jwt.encode(
        {"user": data.__dict__(), "exp": expiration_date},
        secret_key,
        algorithm="HS256"
    )
    return token


def parserToken(secret_key: str, token: str, data: Type[Any]) -> Any:
    decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
    return data(decoded_token["user"])
