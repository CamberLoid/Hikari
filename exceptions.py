import sys,logging,requests
class badAuthException(Exception):
    pass
class invalidCredException(Exception):
    pass

class FriendError(Exception):
    msg = {
        604: 'You can\'t be friends with yourself ;_;',
        401: 'This user does not exist', # 以下都是待抓包
        0: 'You have added this user', 
        1: 'Reached Limit'
    }
    def __init__(self,*args,**kwargs):
        if len(args) != 0: 
            assert type(args[0]) == requests.exceptions.HTTPError
            self.response = args[0].response
            self.errCode = self.response.json().get('error_code',None)
            if self.errCode != None: 
                self.message = self.msg[self.errCode]
            else: self.message = 'Unknown Error'