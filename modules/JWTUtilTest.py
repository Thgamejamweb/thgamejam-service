from datetime import datetime

from config.conf import settings
from core.router_register import UserContext
from modules.JWTUtil import generateToken, parserToken

if __name__ == '__main__':
    conf = settings.get()
    token = generateToken(conf.jwt.secret_key, UserContext(userid=1), 1)
    print(conf.jwt.expiration_time)
    print(token)
    print(parserToken(conf.jwt.secret_key, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJpZCI6MX0sImV4cCI6MTY4Njc1MTEyMn0.FOr_LeNfwplg-_r1xavOkiP-0Hpgfu8coeoeIVde81w", UserContext).__dict__())
