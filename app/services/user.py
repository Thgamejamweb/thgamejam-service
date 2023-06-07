from app.modules.router_register.router_register import register_fastapi_route, parse_request, parse_reply
from thgamejam.api.user.user_pb2_http import UserServicer, register_user_http_server
from thgamejam.api.user import user_pb2 as thgamejam_dot_api_dot_user_dot_user__pb2


class UserServiceImpl(UserServicer):

    def test(self,
             request: thgamejam_dot_api_dot_user_dot_user__pb2.TestRequest) -> thgamejam_dot_api_dot_user_dot_user__pb2.TestReply:
        reply = thgamejam_dot_api_dot_user_dot_user__pb2.TestReply()
        reply.test1 = request.test
        return reply


register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
