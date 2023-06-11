from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

from core.router_register import register_fastapi_route, parse_request, parse_reply
from api.thgamejam.user.user_pb2_http import UserServicer, register_user_http_server
from api.thgamejam.user import user_pb2


class UserServiceImpl(UserServicer):

    def test(self,
             request: google_dot_protobuf_dot_empty__pb2.Empty) -> user_pb2.TestReply:
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply


register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
