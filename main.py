import glob
import importlib

import uvicorn

from core.router_register import app

service_file = glob.glob('services/*.py')

if __name__ == '__main__':
    # services注入
    for file in service_file:
        module_name = file[:-3].replace('\\', '.')
        module = importlib.import_module(module_name)
    uvicorn.run(app)
