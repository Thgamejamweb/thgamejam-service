from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from core.router_register import register_fastapi_route, parse_request, parse_reply
from api.thgamejam.user.user_pb2_http import UserServicer, register_user_http_server
from api.thgamejam.user import user_pb2, user_pb2 as api_dot_thgamejam_dot_user_dot_user__pb2
from modles.base_model import CustomSession
from modles.user import User


class UserServiceImpl(UserServicer):

    def testC(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply

    def testR(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        engine = create_engine(settings.DATA_BASE_URL)
        Session = sessionmaker(bind=engine, class_=CustomSession)
        session = Session()
        user = session.query(User).filter(User.id == 1, User.deleted != True).all()
        print(user)
        session.commit()
        session.close()
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply

    def testU(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        pass

    def testD(self,
              request: google_dot_protobuf_dot_empty__pb2.Empty) -> api_dot_thgamejam_dot_user_dot_user__pb2.TestReply:
        engine = create_engine(settings.DATA_BASE_URL)
        Session = sessionmaker(bind=engine, class_=CustomSession)
        session = Session()
        user = session.query(User).get(2)
        session.delete(user)
        user1 = session.query(User).get(2)
        print(user1.deleted)
        session.commit()
        reply = user_pb2.TestReply()
        reply.test1 = 1
        return reply


register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
