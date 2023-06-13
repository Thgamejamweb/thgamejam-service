from Crypto.PublicKey import RSA

from api.thgamejam.user.user_pb2 import GetUserPublicKeyReply, GetUserPublicKeyRequest, LoginRequest, LoginReply, \
    UserInfo
from core.context import request_context, UserContext
from core.router_register import register_fastapi_route, parse_request, parse_reply
from api.thgamejam.user.user_pb2_http import UserServicer, register_user_http_server
from dao.user_dao import get_userinfo_by_username, update_userinfo, verify_user_password
from database.mysql import database


class UserServiceImpl(UserServicer):

    def GetUserPublicKey(self, request: GetUserPublicKeyRequest) -> GetUserPublicKeyReply:
        # 获取session
        session = database.get_db_session()
        user = get_userinfo_by_username(request.username, session)

        # 验证公私钥是否存在
        if user.public_key is None:
            key = RSA.generate(2048)
            user.private_key = key.export_key().decode('utf-8')
            user.public_key = key.publickey().export_key().decode('utf-8')

            update_userinfo(user, session)

            return GetUserPublicKeyReply(public_key=user.public_key)
        else:
            return GetUserPublicKeyReply(public_key=user.public_key)

    def Login(self, request: LoginRequest) -> LoginReply:
        session = database.get_db_session()
        user = verify_user_password(request.username, request.password, session)

        # request_context.set(UserContext(userid=user.id))

        request_context.set(UserContext(userid=user.id))

        return LoginReply(user=UserInfo(username=user.name))


register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
