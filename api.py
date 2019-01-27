import requests,requests_oauthlib
import asyncio,sys,os,json,time,traceback
from pprint import pprint
from base64 import b64encode,b64decode
from . import exceptions

arcauth = "https://arcapi.lowiro.com/4/auth/login"
arcapi = {
    'base': 'https://arcapi.lowiro.com/4/',
    'auth': 'auth/login',
    'me': '',
    'me_aggerate': 'compose/aggregate?calls=[{ "endpoint": "user/me", "id": 0 }]',
    'addFriend': '',#Friend_Code
    'delFriend': '',#Friend_ID
    'getSongRankGlobal': '',
    'getSongRankMe': ''
}

FakeHeader = {
    'AppVersion': '1.9.0',
    'User-Agent': '	Arc-mobile/1.9.0.0 CFNetwork/975.0.3 Darwin/18.2.0',
    ''
}

aggerateCode = {
    
}
props = json.load(open('arc.json',encoding='UTF-8'))

"""
    Cambot.modules.Hikari
    Version: v2.beta0x01
    重写代码+方法
"""
class Arcaea(object):
    def __init__(self,auth=None,cred=None,pswd=None,**kwargs):
        """
        Todo: Load Config
        """
        self._auth = auth
        if self._auth is None:
            self._auth = self.getAuth(cred,pswd)
        raw = self.getMe()
        self._friendList = raw['value']['friends']

        #pprint(self.Datafetch())    
    @classmethod
    def getAuth(cls,cred,pswd):
        """
        在没有auth或auth过期的时候，使用该方法获取bearer auth
        """
        toencode = cred+":"+pswd
        headers = {
              'Authorization': 'Basic ' + b64encode(
                  toencode.encode('ascii')).decode(),
              'DeviceId': FakeHeader['DeviceID'],
              'AppVersion': FakeHeader['AppVer']}
        po = requests.post(arcauth,headers=headers)
        try:
            po.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise exceptions.invalidCredException()
        if po.json()['success']==True:  
            return po.json()['access_token']
        else:
            raise exceptions.invalidCredException()
    
    def addFriend(self,friend_code):
        header = FakeHeader + {}
        postForm = "friend_id = {}".format(friend_code)
        

    
    def delFriend(self,friend_id):
        pass
    
    def getAggregate(self,*args, **kwargs):
        pass