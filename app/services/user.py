from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

from thgamejam.api.user.user_pb2_http import UserServicer
from thgamejam.api.user import user_pb2 as thgamejam_dot_api_dot_user_dot_user__pb2


class UserServiceImpl(UserServicer):

    def test(self,
             request: google_dot_protobuf_dot_empty__pb2) -> thgamejam_dot_api_dot_user_dot_user__pb2.TestReply:
        reply = thgamejam_dot_api_dot_user_dot_user__pb2.TestReply()
        reply.test1 = "1"
        return reply
