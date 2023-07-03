from fastapi import HTTPException

from api.thgamejam.file.file_pb2 import GetUploadUrlRequest, GetUploadReply, GetDownloadUrlRequest, GetDownloadUrlReply, \
    GetDownloadUrlByStrRequest
from api.thgamejam.file.file_pb2_http import FileServicer, register_file_http_server
from core.router_register import parse_request, parse_reply, register_fastapi_route, request_context
from dao.file_dao import verify_file_eTag, create_fileinfo, update_file_info, get_file_info_by_id, \
    get_file_info_by_name, get_file_info_by_tag
from core.app import instance
from modles.file_entity import FileEntity


class FileServiceImpl(FileServicer):
    def GetUploadUrl(self, request: GetUploadUrlRequest) -> GetUploadReply:
        session = instance.database.get_db_session()
        file = verify_file_eTag(request.e_tag, session)

        if file is not None:
            if file.user_id is None:
                file.user_id = request_context.get().userid
                update_file_info(file, session)

        url = instance.minio_client.get_minio_client().presigned_put_object('web', request.e_tag)
        if file.is_Upload is False:
            return GetUploadReply(id=file.id, url=url)

        file = FileEntity()
        file.file_name = request.file_name
        file.e_tag = request.e_tag
        file.user_id = request_context.get().userid

        create_fileinfo(file, session)

        return GetUploadReply(id=file.id, url=url)

    def GetDownloadUrlByid(self, request: GetDownloadUrlRequest) -> GetDownloadUrlReply:
        session = instance.database.get_db_session()
        file = get_file_info_by_id(request.id, session)
        if file is None:
            raise HTTPException(status_code=404, detail="file not found")

        url = instance.minio_client.get_minio_client().presigned_put_object('web', file.e_tag)
        return GetDownloadUrlReply(url=url)

    def GetDownloadUrlByFileName(self, request: GetDownloadUrlByStrRequest) -> GetDownloadUrlReply:
        session = instance.database.get_db_session()
        file = get_file_info_by_name(request.info, session)
        if file is None:
            raise HTTPException(status_code=404, detail="file not found")

        url = instance.minio_client.get_minio_client().presigned_put_object('web', file.e_tag)
        return GetDownloadUrlReply(url=url)

    def GetDownloadUrlByTag(self, request: GetDownloadUrlByStrRequest) -> GetDownloadUrlReply:
        session = instance.database.get_db_session()
        file = get_file_info_by_tag(request.info, session)
        if file is None:
            raise HTTPException(status_code=404, detail="file not found")

        url = instance.minio_client.get_minio_client().presigned_put_object('web', file.e_tag)
        return GetDownloadUrlReply(url=url)


register_file_http_server(register_fastapi_route, FileServiceImpl(), parse_request, parse_reply)
