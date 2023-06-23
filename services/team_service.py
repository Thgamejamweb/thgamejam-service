from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.team.team_pb2 import GetTeamNumberListRequest, GetTeamNumberListReply, SetTeamNumberRequest, \
    CreateTeamRequest, CreateTeamReply, DeleteTeamRequest, ChangeTeamNameRequest, UserInfo
from api.thgamejam.team.team_pb2_http import TeamServicer, register_team_http_server
from core.app import instance
from core.router_register import parse_request, parse_reply, register_fastapi_route, request_context
from dao.team_dao import get_team_number_by_team_id, create_team


class TeamServiceImpl(TeamServicer):
    def GetTeamNumberList(self, request: GetTeamNumberListRequest) -> GetTeamNumberListReply:
        session = instance.database.get_db_session()
        users = get_team_number_by_team_id(request.team_id, session)

        user_list = []
        for user in users:
            user_list.append(UserInfo(id=user.id, name=user.name, avatar_url=user.avatar_image))

        return GetTeamNumberListReply(list=user_list)

    def JoinTeam(self, request: SetTeamNumberRequest) -> Empty:
        pass

    def AddTeamNumber(self, request: SetTeamNumberRequest) -> Empty:
        pass

    def DeleteTeamNumber(self, request: SetTeamNumberRequest) -> Empty:
        pass

    def CreateTeam(self, request: CreateTeamRequest) -> CreateTeamReply:
        session = instance.database.get_db_session()

        team = create_team(request.name, request_context.get().userid, session)
        if team is None:
            raise HTTPException(status_code=409, detail="TeamName has exist")

        return CreateTeamReply(team_id=team.id)

    def DeleteTeam(self, request: DeleteTeamRequest) -> Empty:
        pass

    def ChangeTeamName(self, request: ChangeTeamNameRequest) -> Empty:
        pass


register_team_http_server(register_fastapi_route, TeamServiceImpl(), parse_request, parse_reply)
