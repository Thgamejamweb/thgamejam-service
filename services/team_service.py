from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.team.team_pb2 import GetTeamNumberListRequest, GetTeamNumberListReply, SetTeamNumberRequest, \
    CreateTeamRequest, CreateTeamReply, DeleteTeamRequest, ChangeTeamNameRequest, UserInfo
from api.thgamejam.team.team_pb2_http import TeamServicer, register_team_http_server
from core.app import instance
from core.router_register import parse_request, parse_reply, register_fastapi_route, request_context
from dao.team_dao import get_team_number_by_team_id, create_team, verify_user_id_team_admin, change_team_name, \
    add_user_into_team, get_user_add_team_info, user_join_team, delete_user_in_team_info
from dao.user_dao import get_userinfo_by_id


class TeamServiceImpl(TeamServicer):
    def GetTeamNumberList(self, request: GetTeamNumberListRequest) -> GetTeamNumberListReply:
        session = instance.database.get_db_session()
        users = get_team_number_by_team_id(request.team_id, session)

        user_list = []
        for user in users:
            user_list.append(UserInfo(id=user.id, name=user.name, avatar_url=user.avatar_image))

        return GetTeamNumberListReply(list=user_list)

    def JoinTeam(self, request: SetTeamNumberRequest) -> Empty:
        session = instance.database.get_db_session()
        user_info = get_user_add_team_info(request_context.get().userid, request.team_id, session)
        if user_info is None:
            raise HTTPException(status_code=404, detail="Add to team error")

        user_join_team(user_info, session)
        return Empty()

    def AddTeamNumber(self, request: SetTeamNumberRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is not True:
            raise HTTPException(status_code=403, detail="Forbidden")

        user = get_userinfo_by_id(request.user_id, session)
        if user is None:
            raise HTTPException(status_code=404, detail="UserInfo not find")

        add_user_into_team(request.user_id, request.team_id, session)
        return Empty()

    def DeleteTeamNumber(self, request: SetTeamNumberRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is not True:
            raise HTTPException(status_code=403, detail="Forbidden")

        delete_user_in_team_info(request.user_id, request.team_id, session)
        return Empty()

    def CreateTeam(self, request: CreateTeamRequest) -> CreateTeamReply:
        session = instance.database.get_db_session()

        team = create_team(request.name, request_context.get().userid, session)
        if team is None:
            raise HTTPException(status_code=409, detail="TeamName has exist")

        return CreateTeamReply(team_id=team.id)

    def DeleteTeam(self, request: DeleteTeamRequest) -> Empty:
        pass

    def ChangeTeamName(self, request: ChangeTeamNameRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is not True:
            raise HTTPException(status_code=403, detail="Forbidden")

        change_team_name(request.team_id, request.new_name, session)

        return Empty()


register_team_http_server(register_fastapi_route, TeamServiceImpl(), parse_request, parse_reply)
