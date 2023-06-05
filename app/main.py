
import uvicorn

from app.services.user import UserServiceImpl
from app.utils.router_register import register_fastapi_route, parse_request, parse_reply, app
from thgamejam.api.user.user_pb2_http import register_user_http_server




# service_file = glob.glob("services/*.py")

if __name__ == '__main__':
    # for file_path in service_file:
    #     module_name = file_path.replace(".py", "").replace("\\", ".")
    #     print(module_name)
    #     module = importlib.import_module(module_name)
    register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
    uvicorn.run(app)
