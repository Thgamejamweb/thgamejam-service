import datetime

from app.utils.JWTUtil import generateToken, parserToken

if __name__ == '__main__':
    token = generateToken("aa", {"a": "a"}, datetime.datetime.utcnow() + datetime.timedelta(seconds=1))
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImEiOiJhIn0sImV4cCI6MTY4NjE0MTg5M30.Iul973bU2PSRLhmndOSJmfN8CYFMcbOdle1qY0f1nDw"
    print(token)
    print(parserToken("aa", token))
