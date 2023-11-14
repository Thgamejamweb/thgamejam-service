from api.thgamejam.chatgpt.aigc_pb2 import UpdateContentRequest, UpdateContentReply
from api.thgamejam.chatgpt.aigc_pb2_http import AigcServicer, register_aigc_http_server
from core.Helper import chat_with_gpt
from core.router_register import register_fastapi_route, parse_request, parse_reply


class AigcServiceImpl(AigcServicer):
    async def UpdateContent(self, request: UpdateContentRequest) -> UpdateContentReply:
        reply = chat_with_gpt(request.content)
        return UpdateContentReply(new_content=reply)


register_aigc_http_server(register_fastapi_route, AigcServiceImpl(), parse_request, parse_reply)
