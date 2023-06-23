import os
from typing import List
from dotenv import load_dotenv
from google.protobuf.json_format import ParseDict
from google.protobuf.message import Message

from config.conf import ConfigReaderFunction

# 加载.env配置文件
load_dotenv()


def get_nested_fields(fields, prefix: str = "") -> List[str]:
    data: List[str] = []
    for field in fields:
        field_name = prefix + field.name

        if field.message_type is not None:
            nested_fields = field.message_type.fields
            nested_prefix = field_name + "."
            data = data + get_nested_fields(nested_fields, prefix=nested_prefix)
        else:
            data.append(field_name)

    return data


def convert_nested_keys(data):
    converted_data = {}
    for key, value in data.items():
        if '.' in key:
            nested_keys = key.split('.')
            nested_dict = converted_data
            for nested_key in nested_keys[:-1]:
                if nested_key not in nested_dict:
                    nested_dict[nested_key] = {}
                nested_dict = nested_dict[nested_key]
            nested_dict[nested_keys[-1]] = value
        else:
            converted_data[key] = value
    return converted_data


def read_env_config() -> ConfigReaderFunction:
    def read_env(m: Message):
        # 获取类型的描述符
        descriptor = m.DESCRIPTOR
        top_level_fields = descriptor.fields
        env_list = get_nested_fields(top_level_fields)

        env = {k: os.getenv(k) for k in env_list if os.getenv(k) is not None}

        data = convert_nested_keys(env)
        ParseDict(data, m)

    return read_env
