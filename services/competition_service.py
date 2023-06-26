from google.protobuf.empty_pb2 import Empty

from api.thgamejam.competition.competition_pb2 import CompetitionListReply, GetUserJoinCompetitionListRequest, \
    GetTeamJoinCompetitionListRequest, CreateCompetitionRequest, CreateCompetitionReply, JoinCompetitionRequest, \
    AddWorksRequest
from api.thgamejam.competition.competition_pb2_http import CompetitionServicer, register_competition_http_server
from core.router_register import register_fastapi_route, parse_reply, parse_request


class CompetitionServiceImpl(CompetitionServicer):

    def GetSignupCompetitionList(self, request: Empty) -> CompetitionListReply:
        pass

    def GetStartCompetitionList(self, request: Empty) -> CompetitionListReply:
        pass

    def GetEndCompetitionList(self, request: Empty) -> CompetitionListReply:
        pass

    def GetUserJoinCompetitionList(self, request: GetUserJoinCompetitionListRequest) -> CompetitionListReply:
        pass

    def GetTeamJoinCompetitionList(self, request: GetTeamJoinCompetitionListRequest) -> CompetitionListReply:
        pass

    def GetUserIsStaff(self, request: Empty) -> Empty:
        pass

    def CreateCompetition(self, request: CreateCompetitionRequest) -> CreateCompetitionReply:
        pass

    def JoinCompetition(self, request: JoinCompetitionRequest) -> Empty:
        pass

    def AddCompetition(self, request: AddWorksRequest) -> Empty:
        pass


register_competition_http_server(register_fastapi_route, CompetitionServiceImpl(), parse_request, parse_reply)
