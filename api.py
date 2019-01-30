import requests,requests_oauthlib
import asyncio,sys,os,json,time,traceback
from pprint import pprint
from base64 import b64encode,b64decode
import exceptions
arcauth = "https://arcapi.lowiro.com/4/auth/login"
arcapi = {
    'base': 'https://arcapi.lowiro.com/4/',
    'auth': 'auth/login',
    'me': 'user/me',
    'aggreate': 'compose/aggregate?calls={}',
    'addFriend': 'friend/me/add', #friend_code, 9 digits, public_accessible
    'delFriend': 'friend/me/delete', #friend_ID , about 6 digit, public_inaccessible
    'getSongRankGlobal': 'score/song?song_id={}&difficulty={}&start=0&limit=10',
    'getSongRankMe': 'score/song/me?song_id={}&difficulty={}&start=4&limit=8',#response may be an empty list
    'getSongRankFriend': 'score/song/friend?song_id={}&difficulty={}&start=0&limit=12'
}

FakeHeader = {
    'AppVersion': '', #从Config中读取
    'User-Agent': 'Arc-mobile/{} CFNetwork/{} Darwin/{}'
}

aggreateCode = {
    # Deprecated
    # me: [{ "endpoint": "user/me", "id": 0 }]
    # 靠生成, 不硬写进去了
}


"""
    Cambot.modules.Hikari
    Version: Arcapiv2.beta0x01 + Hikari + Fracture(OnDevelop)
    重写代码+方法
"""
class Arcaea(object):
    def debug(self):
        return [self.__cred,self.__pswd,self.__auth]
    def __init__(self,path='config.json',precheck = True,byweb = False,**kwargs):
        # Initialize via File
        if precheck: 
            self.__precheck(path)
        self.__getProp(path)
        self.__path = path
        self.__cred = self._prop.get('adminCred')
        self.__pswd = self._prop.get('adminPswd')
        self.__auth = self._prop.get('adminAuth')
        # headers初始化
        if byweb: FakeHeader['User-Agent'] = 'web'
        else: 
            FakeHeader['User-Agent'] = FakeHeader['User-Agent'].format(
            self._prop['arcVer']['Arc-mobile'],
            self._prop['arcVer']['CFNetwork'],
            self._prop['arcVer']['Darwin'])
            FakeHeader['AppVer'] = self._prop.get("AppVer")
        if self.__auth == None:
            if self.__cred is None or self.__pswd is None:
                raise exceptions.badAuthException("Invalid Login Infomation")
            self.__auth = self.getAuth(self.__cred,self.__pswd)
            self._prop['adminAuth'] = self.__auth
            self.__setProp()
               
        #pprint(self.Datafetch())
    def __getProp(self,path):
        """
        读取config.json所设置的属性
        """
        with open(path,encoding='UTF-8') as f:
            self._prop = json.load(f)
    def __setProp(self):
        """
        写入config.json
        """ 
        path = self.__path
        with open(path,mode = 'w',encoding='UTF-8') as f:
            json.dump(self._prop,f)
    
    def getAuth(self,cred,pswd):
        """
        在没有auth或auth过期的时候，使用该方法获取bearer auth
        """
        import uuid
        toencode = cred+":"+pswd
        if FakeHeader['AppVersion'] == 'web': deviceid = 'web'
        else: 
            if self._prop.get('uuid') != None: 
                deviceid = self._prop.get('uuid')
            else: 
                deviceid = str(uuid.uuid4()).upper()
                self._prop['uuid'] = deviceid
                self.__setProp()
        headers = {
              'Authorization': 'Basic ' + b64encode(
                  toencode.encode('ascii')).decode(),
              'DeviceId': deviceid,
              'AppVersion': FakeHeader['AppVer']}
        po = requests.post(arcauth,headers=headers)
        try:
            po.raise_for_status()
        except:
            print(po.text)
            print(po.json())
        if po.json()['success']==True: return po.json()['access_token']
        else: raise exceptions.invalidCredException()
        
    def getMe(self):
        """获取个人信息，若无异常返回一个dict对象"""
        headers = self.getHeader({'Authorization':'Bearer '+self.__auth})
        url = arcapi['aggreate'].format(self.generateAggregate(arcapi['me']))
        req = requests.get(url,headers = headers)
        req.raise_for_status()
        return req.json()['value']

    def addFriend(self,friend_code):
        assert type(friend_code) is str
        url = arcapi['base']+arcapi['addFriend']
        headers = self.getHeader({'Authorization':'Bearer '+self.__auth})
        postForm = {"friend_code":friend_code}
        req = requests.post(url,headers=headers,params=postForm)
        try:
            req.raise_for_status()
        except Exception as e:
            print(req.text)
            raise e
        if req.json()['success'] == False: return req.json()
        else: return req.json()['value']['friends']
        
    def delFriend(self,friend_id):
        assert type(friend_id) is str
        url = arcapi['base']+arcapi['delFriend']
        headers = (FakeHeader.copy()).update({'Authorization':'Bearer '+self.__auth})
        postForm = {"friend_id":friend_id}
        req = requests.post(url,headers = headers,data=postForm)
        req.raise_for_status()
        if req.json()['success'] == True: return True
        else: return False

    async def reAuth(self):
        self._auth = await self.getAuth(self.__cred,self.__pswd)

    def getSongRank(self,song_id,method = ''):
        
        pass
    def __precheck(self,path):
        """前置检查"""
        if not os.path.exists(path): raise OSError("不存在指定配置文件")
        return True

    def getHeader(self,headers):
        """获取HTTP头"""
        assert type(headers) is dict
        return (FakeHeader.copy()).update(headers)
    
    @classmethod
    def generateAggregate(cls,*args, **kwargs):
        """生成endpoint"""
        query = args
        if query == None: query = ['user/me']
        aggregate = []
        s = 0
        for i in query:
            aggregate.append({'endpoint':i,'id':s})
            s+=1
        return aggregate
    
