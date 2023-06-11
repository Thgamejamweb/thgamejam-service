import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# 加载.env配置文件
load_dotenv()


class Config(BaseSettings):
    DATA_BASE_URL = os.getenv("DATA_BASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_EXPIRATION_TIME = os.getenv("JWT_EXPIRATION_TIME")
    POOL_TIMEOUT = os.getenv("POOL_TIMEOUT")
    POOL_SIZE = os.getenv("POOL_SIZE")
    POOL_RECYCLE = os.getenv("POOL_RECYCLE")
    CONNECT_TIMEOUT = os.getenv("CONNECT_TIMEOUT")


settings = Config()
