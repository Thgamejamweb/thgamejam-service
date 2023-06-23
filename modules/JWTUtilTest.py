from modules.JWTUtil import generateToken


class UserContext:
    def __init__(self, userid: int):
        self.userid = userid

    def __dict__(self):
        return {
            'userid': self.userid
        }


if __name__ == '__main__':
    token = generateToken("in_my_long_forgotten_cloistered_sleep", UserContext(userid=3), 604800)
    print(token)
