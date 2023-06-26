from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.competition.competition_pb2 import CompetitionListReply, GetUserJoinCompetitionListRequest, \
    GetTeamJoinCompetitionListRequest, CreateCompetitionRequest, CreateCompetitionReply, JoinCompetitionRequest, \
    AddWorksRequest, CompetitionInfo
from api.thgamejam.competition.competition_pb2_http import CompetitionServicer, register_competition_http_server
from core.app import instance
from core.router_register import register_fastapi_route, parse_reply, parse_request, request_context
from dao.competition_dao import get_competition_list_by_userid, get_competition_info_by_team_id, \
    create_competition_info, create_competition, team_join_competition, add_team_works_to_competition
from dao.team_dao import verify_user_id_team_admin
from dao.user_dao import get_userinfo_by_id
from modles.competition_entity import CompetitionEntity


class CompetitionServiceImpl(CompetitionServicer):

    def GetSignupCompetitionList(self, request: Empty) -> CompetitionListReply:
        pass

    def GetStartCompetitionList(self, request: Empty) -> CompetitionListReply:
        pass

    def GetEndCompetitionList(self, request: Empty) -> CompetitionListReply:
        pass

    def GetUserJoinCompetitionList(self, request: GetUserJoinCompetitionListRequest) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_competition_list_by_userid(request.user_id, session)

        competitions = {}
        for competition in competition_info_list:
            competitions[competition.id] = CompetitionInfo(id=competition.id, name=competition.name,
                                                           staff_id=competition.staff_id,
                                                           description=competition.description,
                                                           header_imageURL=competition.header_imageURL)

        return CompetitionListReply(list=list(competitions.values()))

    def GetTeamJoinCompetitionList(self, request: GetTeamJoinCompetitionListRequest) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_competition_info_by_team_id(request.team_id, session)

        competitions = []
        for competition in competition_info_list:
            competitions.append(CompetitionInfo(id=competition.id, name=competition.name,
                                                staff_id=competition.staff_id,
                                                description=competition.description,
                                                header_imageURL=competition.header_imageURL))

        return CompetitionListReply(list=competitions)

    def GetUserIsStaff(self, request: Empty) -> Empty:
        session = instance.database.get_db_session()
        user = get_userinfo_by_id(request_context.get().userid, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not find")

        if user.is_staff is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        return Empty()

    def CreateCompetition(self, request: CreateCompetitionRequest) -> CreateCompetitionReply:
        session = instance.database.get_db_session()
        user = get_userinfo_by_id(request_context.get().userid, session)
        if user is None:
            raise HTTPException(status_code=404, detail="User not find")

        if user.is_staff is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        # TODO 时间转换
        competition = create_competition(CompetitionEntity(name=request.name, description=request.description,
                                                           header_imageURL=request.header_imageURL,
                                                           staff_id=request_context.get().userid), session)

        create_competition_info(competition.id, request.content, session)

        return CreateCompetitionReply(competition_id=competition.id)

    def JoinCompetition(self, request: JoinCompetitionRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        team_join_competition(request.team_id, request.competition_id, session)

        return Empty()

    def AddCompetition(self, request: AddWorksRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        add_team_works_to_competition(request.competition_id, request.works_id, request.works_id, session)

        return Empty()


register_competition_http_server(register_fastapi_route, CompetitionServiceImpl(), parse_request, parse_reply)
