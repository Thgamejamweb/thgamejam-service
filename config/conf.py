import copy
import json
from typing import Callable, List, Any
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson

from config.conf_pb2 import Bootstrap

ConfigReaderFunction = Callable[[Message], Any]


class Config(object):
    config_reader_list: List[ConfigReaderFunction]
    instance: Bootstrap

    def __init__(self):
        self.config_reader_list = []
        self.instance = Bootstrap()

    def add_config_reader(self, config_reader: ConfigReaderFunction):
        self.config_reader_list.append(config_reader)

    def read(self):
        mge = Bootstrap()
        for func in self.config_reader_list:
            func(mge)
        self.instance = mge

    def get(self) -> Bootstrap:
        return copy.deepcopy(self.instance)

    def __str__(self):
        func_names = [func.__name__ for func in self.config_reader_list]
        func_json = json.dumps(func_names)
        mge_json = MessageToJson(self.instance, including_default_value_fields=True)
        data = f'{{ "config_reader_list": {func_json}, "instance": {mge_json} }}'
        parsed_json = json.loads(data)
        return json.dumps(parsed_json, indent=2)


settings = Config()
