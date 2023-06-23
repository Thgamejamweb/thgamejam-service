import tomllib
from typing import Dict
from google.protobuf.message import Message
from google.protobuf.json_format import ParseDict

from config.conf import ConfigReaderFunction


def convert_dict_values_to_str(data):
    if isinstance(data, Dict):
        return {k: convert_dict_values_to_str(v) for k, v in data.items()}
    else:
        return str(data)


def read_toml_config(file) -> ConfigReaderFunction:
    def read_toml(m: Message):
        with open(file, "rb") as f:
            toml = tomllib.load(f)
            data = convert_dict_values_to_str(toml)
            ParseDict(data, m)

    return read_toml
