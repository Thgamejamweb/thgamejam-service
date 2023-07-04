import random
import string

from fastapi import HTTPException
from google.protobuf.empty_pb2 import Empty

from api.thgamejam.works.works_pb2 import CreateWorksRequest, UpdateWorksRequest, WorksIdRequest, GetWorksByNameRequest, \
    CreateWorksReply, WorksInfo, GetWorksListByTeamNameReply, WorkDetails, DeleteWorksByIdRequest, GetWorksByIdRequest, \
    GetWorksListByTeamIdReply, GetRandom4DateReply, getWorksByReverseIdReply, GetUserIsTeamAdminRequest
from api.thgamejam.works.works_pb2_http import WorksServicer, register_works_http_server
from core.app import instance
from dao.team_dao import verify_user_id_team_admin, get_team_name_by_team_id
from dao.works_dao import *
from core.router_register import parse_request, parse_reply, register_fastapi_route, request_context


class WorksServiceImpl(WorksServicer):

    def GetRandom4DateRequest(self, request: Empty) -> GetRandom4DateReply:
        print("aaa")
        session = instance.database.get_db_session()
        work_list = get_random_four_date(session)
        size = len(work_list)
        print(size)
        works = []
        for i in range(4):
            kk = work_list[i]
            team = get_team_name_by_team_id(kk.team_id, session)

            works.append(WorksInfo(id=kk.id, team_id=kk.team_id, work_name=kk.name, team_name=team.name,
                                   header_imageURL=kk.header_imageURL))
        return GetRandom4DateReply(works_list=works)

    def GetWorksByReverseIdRequest(self, request: Empty) -> getWorksByReverseIdReply:
        session = instance.database.get_db_session()
        work_list: list[WorksEntity] = get_reserve_eight_date(session)
        size = len(work_list)
        works = []
        for i in range(8):
            kk = work_list[i]
            team = get_team_name_by_team_id(kk.team_id, session)
            works.append(WorksInfo(id=kk.id, team_id=kk.team_id, work_name=kk.name, team_name=team.name,
                                   header_imageURL=kk.header_imageURL))
        return getWorksByReverseIdReply(works_list=works)

    def GetWorksListByTeamId(self, request: GetWorksByIdRequest) -> GetWorksListByTeamIdReply:
        session = instance.database.get_db_session()
        works = get_works_list_by_term_id(request.team_id, session)
        team = get_team_name_by_team_id(request.team_id, session)
        if works is None:
            raise HTTPException(status_code=404, detail="Team not exist")
        works_list = []
        for woks in works:
            works_list.append(
                WorksInfo(id=woks.id, team_id=woks.team_id, work_name=woks.name, team_name=team.name,
                          header_imageURL=woks.header_imageURL))

        return GetWorksListByTeamIdReply(work_list=works_list)

    def DeleteWorksById(self, request: DeleteWorksByIdRequest) -> Empty:
        session = instance.database.get_db_session()

        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        delete_works_by_id(request.work_id, session)
        return Empty()

    def GetWorksById(self, request: WorksIdRequest) -> WorksInfo:
        session = instance.database.get_db_session()
        works = get_works_by_id(request.works_id, session)
        team = get_team_name_by_team_id(works.team_id, session)
        return WorksInfo(work_name=works.name, team_id=team.id, team_name=team.name,
                         header_imageURL=works.header_imageURL)

    def GetWorksByName(self, request: GetWorksByNameRequest) -> WorksInfo | None:
        session = instance.database.get_db_session()
        work = get_works_by_name(request.name, session=session)
        team = get_team_name_by_team_id(work.team_id, session)
        if team is not None:
            return WorksInfo(id=work.id, team_id=work.team_id, work_name=work.name,
                             header_imageURL=work.header_imageURL, team_name=team.name)
        return None

    def GetWorksListByTeamName(self, request: GetWorksByNameRequest) -> GetWorksListByTeamNameReply:
        session = instance.database.get_db_session()
        works = get_works_list_by_term_name(request.name, session)
        if works is None:
            raise HTTPException(status_code=404, detail="Team not exist")

        works_list = []
        for woks in works:
            works_list.append(WorksInfo(id=woks.id, team_id=woks.team_id, work_name=woks.name, team_name=request.name,
                                        header_imageURL=woks.header_imageURL))

        return GetWorksListByTeamNameReply(work_list=works_list)

    def GetWorksDetailsById(self, request: WorksIdRequest) -> WorkDetails:
        session = instance.database.get_db_session()
        work_info = get_works_info_by_id(request.works_id, session)
        if work_info is None:
            raise HTTPException(status_code=404, detail="Works not find")

        works = get_works_by_id(request.works_id, session)
        team = get_team_name_by_team_id(work_info.team_id, session)
        return WorkDetails(works_id=works.id, team_id=team.id, content=work_info.content, works_name=works.name,
                           header_imageURL=works.header_imageURL, file_id=work_info.file_id,
                           image_url_list=work_info.image_url_list)

    # 创建作品
    def CreateWorks(self, request: CreateWorksRequest) -> CreateWorksReply | None:
        session = instance.database.get_db_session()
        # 是否是队长
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")

        work = create_works(name=request.name, header_imageURL=request.header_imageURL, team_id=request.team_id,
                            session=session)
        if work is not None:
            # 将数组转换为字符串
            url_list: string = ",".join(request.image_url_list)
            work_info = WorksInfoEntity(request.team_id, url_list, request.content, request.file_id,
                                        work.id)
            create_works_info(work_info, session)
            return CreateWorksReply(id=work.id)
        else:
            raise HTTPException(status_code=500, detail="作品名重复")

    # 更新作品
    def UpdateWorks(self, request: UpdateWorksRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin is False:
            raise HTTPException(status_code=403, detail="Forbidden")
        works = WorksEntity(request.team_id, request.header_imageURL, request.name)
        url_list: str = ",".join(request.image_url_list)
        works_info = WorksInfoEntity(request.team_id, url_list, request.content, request.file_id,
                                     request.works_id)
        update_work_info(works_info, session)
        update_work(works, session)
        return Empty()

    def GetUserIsTeamAdmin(self, request: GetUserIsTeamAdminRequest) -> Empty:
        session = instance.database.get_db_session()
        is_admin = verify_user_id_team_admin(request_context.get().userid, request.team_id, session)
        if is_admin:
            return Empty()

        raise HTTPException(status_code=403)


register_works_http_server(register_fastapi_route, WorksServiceImpl(), parse_request, parse_reply)
