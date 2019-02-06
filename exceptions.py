import sys,logging,requests
class badAuthException(Exception):
    pass
class invalidCredException(Exception):
    pass

friendErrMsg = {
        604: 'You can\'t be friends with yourself ;_;',
        401: 'This user does not exist', # 以下都是待抓包
        602: 'You have added this user', 
        1: 'Reached Limit'
    }
class FriendError(Exception):
    
    def __init__(self,error,*args,**kwargs):
        #assert error == requests.exceptions.HTTPError
        self.response = error.response
        self.errCode = self.response.json().get('error_code',None)
        if self.errCode != None: 
            self.message = friendErrMsg.get(self.errCode,'Unknown')
        else: self.message = 'Unknown Error'
        super().__init__(*args,**kwargs)