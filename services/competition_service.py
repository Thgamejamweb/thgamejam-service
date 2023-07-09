from datetime import datetime

from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.competition.competition_pb2 import CompetitionListReply, GetUserJoinCompetitionListRequest, \
    GetTeamJoinCompetitionListRequest, CreateCompetitionRequest, CreateCompetitionReply, JoinCompetitionRequest, \
    AddWorksRequest, CompetitionInfo, GetWorksListByCompetitionIdRequest, WorksInfoReply, WorksListReply, \
    CompetitionDetailReply, GetCompetitionDetailInfoRequest
from api.thgamejam.competition.competition_pb2_http import CompetitionServicer, register_competition_http_server
from core.app import instance
from core.router_register import register_fastapi_route, parse_reply, parse_request, request_context
from dao.competition_dao import get_competition_list_by_userid, get_competition_info_by_team_id, \
    create_competition_info, create_competition, team_join_competition, add_team_works_to_competition, \
    get_signup_competition_list, get_start_competition_list, get_score_competition_list, \
    get_all_upload_works_by_competitionId, get_competition_detail_info_byid, get_detail_competition_info_byid
from dao.team_dao import verify_user_id_team_admin, get_team_name_by_team_id
from dao.user_dao import get_userinfo_by_id
from dao.works_dao import get_works_by_id
from modles.competition_entity import CompetitionEntity


class CompetitionServiceImpl(CompetitionServicer):

    def GetWorksListByCompetitionId(self, request: GetWorksListByCompetitionIdRequest) -> WorksListReply:
        session = instance.database.get_db_session()
        works_ids = get_all_upload_works_by_competitionId(request.competition_id, session)

        works_list = []
        for works in works_ids:
            works_info = get_works_by_id(works.works_id, session)
            team_info = get_team_name_by_team_id(works_info.team_id, session)
            works_list.append(
                WorksInfoReply(works_id=works_info.id, works_name=works_info.name, team_name=team_info.name,
                               header_imageURL=works_info.header_imageURL))

        return WorksListReply(list=works_list)

    def GetSignupCompetitionList(self, request: Empty) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_signup_competition_list(session)

        competitions = []
        for competition in competition_info_list:
            user = get_userinfo_by_id(competition.staff_id, session)
            competitions.append(CompetitionInfo(id=competition.id, name=competition.name,
                                                staff_name=user.name,
                                                description=competition.description,
                                                header_imageURL=competition.header_imageURL))

        return CompetitionListReply(list=competitions)

    def GetStartCompetitionList(self, request: Empty) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_start_competition_list(session)

        competitions = []
        for competition in competition_info_list:
            user = get_userinfo_by_id(competition.staff_id, session)
            competitions.append(CompetitionInfo(id=competition.id, name=competition.name,
                                                staff_name=user.name,
                                                description=competition.description,
                                                header_imageURL=competition.header_imageURL))

        return CompetitionListReply(list=competitions)

    def GetEndCompetitionList(self, request: Empty) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_score_competition_list(session)

        competitions = []
        for competition in competition_info_list:
            user = get_userinfo_by_id(competition.staff_id, session)
            competitions.append(CompetitionInfo(id=competition.id, name=competition.name,
                                                staff_name=user.name,
                                                description=competition.description,
                                                header_imageURL=competition.header_imageURL))

        return CompetitionListReply(list=competitions)

    def GetUserJoinCompetitionList(self, request: GetUserJoinCompetitionListRequest) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_competition_list_by_userid(request.user_id, session)

        competitions = {}
        for competition in competition_info_list:
            user = get_userinfo_by_id(competition.staff_id, session)
            competitions[competition.id] = CompetitionInfo(id=competition.id, name=competition.name,
                                                           staff_name=user.name,
                                                           description=competition.description,
                                                           header_imageURL=competition.header_imageURL)

        return CompetitionListReply(list=list(competitions.values()))

    def GetTeamJoinCompetitionList(self, request: GetTeamJoinCompetitionListRequest) -> CompetitionListReply:
        session = instance.database.get_db_session()
        competition_info_list = get_competition_info_by_team_id(request.team_id, session)

        competitions = []
        for competition in competition_info_list:
            user = get_userinfo_by_id(competition.staff_id, session)
            competitions.append(CompetitionInfo(id=competition.id, name=competition.name,
                                                staff_name=user.name,
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

        competition = create_competition(CompetitionEntity(name=request.name, description=request.description,
                                                           header_imageURL=request.header_imageURL,
                                                           signup_start_date=datetime.strptime(
                                                               request.signup_start_date, '%Y-%m-%d %H:%M:%S'),
                                                           signup_end_date=datetime.strptime(request.signup_end_date,
                                                                                             '%Y-%m-%d %H:%M:%S'),
                                                           start_date=datetime.strptime(request.start_date,
                                                                                        '%Y-%m-%d %H:%M:%S'),
                                                           end_date=datetime.strptime(request.end_date,
                                                                                      '%Y-%m-%d %H:%M:%S'),
                                                           score_start_date=datetime.strptime(request.score_start_date,
                                                                                              '%Y-%m-%d %H:%M:%S'),
                                                           score_end_date=datetime.strptime(request.score_end_date,
                                                                                            '%Y-%m-%d %H:%M:%S'),
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

    def AddCompetitionWorks(self, request: AddWorksRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            print(request.works_id)
            raise HTTPException(status_code=403, detail="Forbidden")

        is_join = add_team_works_to_competition(request.competition_id, request.team_id, request.works_id, session)
        if is_join is False:
            raise HTTPException(status_code=403, detail="join error")

        return Empty()

    def GetCompetitionDetailInfo(self, request: GetCompetitionDetailInfoRequest) -> CompetitionDetailReply:
        session = instance.database.get_db_session()
        competition = get_competition_detail_info_byid(request.competition_id, session)
        competition_info = get_detail_competition_info_byid(request.competition_id, session)
        staff = get_userinfo_by_id(competition.staff_id, session)
        works_ids = get_all_upload_works_by_competitionId(request.competition_id, session)

        works_list = []
        for works in works_ids:
            works_info = get_works_by_id(works.works_id, session)
            team_info = get_team_name_by_team_id(works_info.team_id, session)
            works_list.append(
                WorksInfoReply(works_id=works_info.id, works_name=works_info.name, team_name=team_info.name,
                               header_imageURL=works_info.header_imageURL))

        is_signup = competition.signup_start_date <= datetime.now() <= competition.signup_end_date
        return CompetitionDetailReply(name=competition.name, context=competition_info.content, is_signup=is_signup,
                                      staff_name=staff.name, description=competition.description,
                                      header_imageURL=competition.header_imageURL, works_list=works_list)


register_competition_http_server(register_fastapi_route, CompetitionServiceImpl(), parse_request, parse_reply)
