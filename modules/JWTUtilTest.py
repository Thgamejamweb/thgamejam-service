from datetime import datetime

from config import settings
from core.router_register import UserContext
from modules.JWTUtil import generateToken, parserToken

if __name__ == '__main__':
    token = generateToken(settings.JWT_SECRET_KEY, UserContext(userid=1), 1)
    print(settings.JWT_EXPIRATION_TIME)
    print(token)
    print(parserToken(settings.JWT_SECRET_KEY, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJpZCI6MX0sImV4cCI6MTY4Njc1MTEyMn0.FOr_LeNfwplg-_r1xavOkiP-0Hpgfu8coeoeIVde81w", UserContext).__dict__())
