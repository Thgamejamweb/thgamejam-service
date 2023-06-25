from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.team.team_pb2 import GetTeamMemberListRequest, GetTeamMemberListReply, SetTeamMemberRequest, \
    CreateTeamRequest, CreateTeamReply, DeleteTeamRequest, ChangeTeamNameRequest, UserInfo, RejectJoinTeamRequest, \
    GetUserJoinAllTeamListRequest, GetUserAllTeamListReply, TeamInfo
from api.thgamejam.team.team_pb2_http import TeamServicer, register_team_http_server
from core.app import instance
from core.router_register import parse_request, parse_reply, register_fastapi_route, request_context
from dao.team_dao import get_team_member_by_team_id, create_team, verify_user_id_team_admin, change_team_name, \
    add_user_into_team, get_user_add_team_info, user_join_team, delete_user_in_team_info, delete_team, delete_team_info, \
    get_join_team_list_by_userid, get_all_not_join_team_list_by_userid
from dao.user_dao import get_userinfo_by_id


class TeamServiceImpl(TeamServicer):
    def GetTeamMemberList(self, request: GetTeamMemberListRequest) -> GetTeamMemberListReply:
        session = instance.database.get_db_session()
        users = get_team_member_by_team_id(request.team_id, session)

        user_list = []
        for user in users:
            user_list.append(UserInfo(id=user.id, name=user.name, avatar_url=user.avatar_image))

        return GetTeamMemberListReply(list=user_list)

    def JoinTeam(self, request: SetTeamMemberRequest) -> Empty:
        session = instance.database.get_db_session()
        user_info = get_user_add_team_info(request_context.get().userid, request.team_id, session)
        if user_info is None:
            raise HTTPException(status_code=404, detail="Add to team error")

        user_join_team(user_info, session)
        return Empty()

    def AddTeamMember(self, request: SetTeamMemberRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        user = get_userinfo_by_id(request.user_id, session)
        if user is None:
            raise HTTPException(status_code=404, detail="UserInfo not find")

        add_user_into_team(request.user_id, request.team_id, session)
        return Empty()

    def DeleteTeamMember(self, request: SetTeamMemberRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
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
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        delete_team(request.team_id, session)
        return Empty()

    def ChangeTeamName(self, request: ChangeTeamNameRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        change_team_name(request.team_id, request.new_name, session)

        return Empty()

    def RejectJoinTeam(self, request: RejectJoinTeamRequest) -> Empty:
        session = instance.database.get_db_session()
        delete_team_info(request.team_id, request_context.get().userid, session)

        return Empty()

    def GetUserJoinAllTeamList(self, request: GetUserJoinAllTeamListRequest) -> GetUserAllTeamListReply:
        session = instance.database.get_db_session()

        team_info_list = get_join_team_list_by_userid(request.user_id, session)

        team_list = []
        for team in team_info_list:
            team_list.append(TeamInfo(team_id=team.id, team_name=team.name))

        return GetUserAllTeamListReply(list=team_list)

    def GetAllRequestTeamList(self, request: Empty) -> GetUserAllTeamListReply:
        session = instance.database.get_db_session()

        team_info_list = get_all_not_join_team_list_by_userid(request_context.get().userid, session)

        team_list = []
        for team in team_info_list:
            team_list.append(TeamInfo(team_id=team.id, team_name=team.name))

        return GetUserAllTeamListReply(list=team_list)


register_team_http_server(register_fastapi_route, TeamServiceImpl(), parse_request, parse_reply)
