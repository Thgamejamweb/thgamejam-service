from fastapi import HTTPException

from api.thgamejam.file.file_pb2 import GetUploadUrlRequest, GetUploadReply, GetDownloadUrlRequest, GetDownloadUrlReply
from api.thgamejam.file.file_pb2_http import FileServicer, register_file_http_server
from core.router_register import parse_request, parse_reply, register_fastapi_route, request_context
from dao.file_dao import verify_file_eTag, create_fileinfo, update_file_info
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
            raise HTTPException(status_code=409, detail="File has exist")

        file = FileEntity()
        file.file_name = request.file_name
        file.e_tag = request.e_tag
        file.user_id = request_context.get().userid

        create_fileinfo(file, session)

        url = instance.minio_client.get_minio_client().presigned_put_object('web', request.e_tag)
        return GetUploadReply(id=file.id, url=url)

    def GetDownloadUrl(self, request: GetDownloadUrlRequest) -> GetDownloadUrlReply:
        print(instance.minio_client.get_minio_client().get_presigned_url('get', 'web', 'QQ浏览器截图20210626100456.png'))
        pass


register_file_http_server(register_fastapi_route, FileServiceImpl(), parse_request, parse_reply)
