from Crypto.PublicKey import RSA
from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.user.user_pb2 import GetUserPublicKeyReply, GetUserPublicKeyRequest, LoginRequest, LoginReply, \
    UserInfo, RegisterUserRequest, RegisterUserReply, ChangePasswordRequest, ChangePasswordReply, GetUserTokenInfoReply, \
    ChangeDescriptionRequest

from core.router_register import register_fastapi_route, parse_request, parse_reply, request_context, UserContext
from api.thgamejam.user.user_pb2_http import UserServicer, register_user_http_server
from dao.user_dao import get_userinfo_by_username, update_userinfo, verify_user_password, create_userinfo, \
    get_userinfo_by_id
from database.mysql import database
from modles.user_entity import UserEntity


class UserServiceImpl(UserServicer):

    def GetUserPublicKey(self, request: GetUserPublicKeyRequest) -> GetUserPublicKeyReply:
        # 获取session
        session = database.get_db_session()
        user = get_userinfo_by_username(request.username, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not exist")

        # 验证公私钥是否存在
        if user.public_key is not None:
            return GetUserPublicKeyReply(public_key=user.public_key)

        key = RSA.generate(2048)
        user.private_key = key.export_key().decode('utf-8')
        user.public_key = key.publickey().export_key().decode('utf-8')

        update_userinfo(user, session)

        return GetUserPublicKeyReply(public_key=user.public_key)

    def Login(self, request: LoginRequest) -> LoginReply:
        session = database.get_db_session()
        user = verify_user_password(request.username, request.password, session)

        request_context.set(UserContext(userid=user.id))

        return LoginReply(user=UserInfo(username=user.name))

    def RegisterUser(self, request: RegisterUserRequest) -> RegisterUserReply:
        session = database.get_db_session()

        user_info = get_userinfo_by_username(request.username, session)
        if user_info is not None:
            raise HTTPException(status_code=404, detail="User has exist")

        key = RSA.generate(2048)
        user = UserEntity()
        user.name = request.username
        user.password = request.password
        user.private_key = key.export_key().decode('utf-8')
        user.public_key = key.publickey().export_key().decode('utf-8')
        u = create_userinfo(user, session)

        request_context.set(UserContext(userid=user.id))
        return RegisterUserReply(id=u.id, username=u.name)

    def ChangePassword(self, request: ChangePasswordRequest) -> ChangePasswordReply:
        session = database.get_db_session()
        user = get_userinfo_by_id(request_context.get().userid, session)
        if user is None:
            raise HTTPException(status_code=404, detail="UserInfo not find")

        if user.password != request.old_password:
            raise HTTPException(status_code=401, detail="Password error")

        user.password = request.new_password
        update_userinfo(user, session)
        return ChangePasswordReply(id=user.id)

    def GetUserTokenInfo(self, request: Empty) -> GetUserTokenInfoReply:
        return GetUserTokenInfoReply(id=request_context.get().userid)

    def ChangeDescription(self, request: ChangeDescriptionRequest) -> Empty:
        session = database.get_db_session()
        user = get_userinfo_by_id(request_context.get().userid, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not find")

        user.description = request.description
        update_userinfo(user, session)
        return Empty()


register_user_http_server(register_fastapi_route, UserServiceImpl(), parse_request, parse_reply)
