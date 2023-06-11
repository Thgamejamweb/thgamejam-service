from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

from core.router_register import register_fastapi_route, parse_request, parse_reply
from api.thgamejam.user.user_pb2_http import UserServicer, register_user_http_server
from api.thgamejam.user import user_pb2, user_pb2 as api_dot_thgamejam_dot_user_dot_user__pb2
from database.mysql import database

from modles.user_entity import UserEntity


class UserServiceImpl(UserServicer):

    def testC(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        session = database.get_db_session()
        data = session.query(UserEntity).all()
        print(data)
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply

    def testR(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply

    def testU(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        pass

    def testD(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply


register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
