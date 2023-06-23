import glob
import importlib

import uvicorn

from config import env_config, toml_config
from config.conf import settings
from core import app
from core.app import App

service_file = glob.glob('services/*.py')

config_toml_path = "config.toml"

if __name__ == '__main__':

    # 配置文件, 顺序toml->env, 后者覆盖前者
    settings.add_config_reader(toml_config.read_toml_config(config_toml_path))
    settings.add_config_reader(env_config.read_env_config())
    settings.read()

    app.instance = App(settings.get())

    # services注入
    for file in service_file:
        module_name = file[:-3].replace('\\', '.')
        module = importlib.import_module(module_name)
    uvicorn.run(app.instance.http)
