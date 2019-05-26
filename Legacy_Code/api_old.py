import requests,requests_oauthlib
import asyncio,sys,os,json,time,traceback,logging
import urllib.parse
from pprint import pprint
from base64 import b64encode,b64decode
from . import exceptions
# 更新API入口
arcauth = "https://arcapi.lowiro.com/5/auth/login"
arcapi = {
    'base': 'https://arcapi.lowiro.com/5/', #不变
    'auth': 'auth/login', #Confirmed
    'me': 'user/me', #<TODO>
    'aggreate': 'compose/aggregate?calls={}',
    'addFriend': 'friend/me/add', #friend_code, 9 digits, public_accessible #<TODO>
    'delFriend': 'friend/me/delete', #friend_ID , about 6 digit, public_inaccessible #<TODO>
    'getSongRank': 'score/song?song_id={}&difficulty={}&start=0&limit=10', # 全球rank获取
    'getSongRankme': 'score/song/me?song_id={}&difficulty={}&start=4&limit=8', # 
    'getSongRankfriend': 'score/song/friend?song_id={}&difficulty={}&start=0&limit=12' # 获取好友Rank
}

FakeHeader = {
    'AppVersion': '', #从Config中读取
    'User-Agent': 'Arc-mobile/{} CFNetwork/{} Darwin/{}'
}

"""
    Cambot.modules.Hikari
    Version: Arcapi(WIP) + HikariV2(0x04)(WIP) + Fracture(WIP)
    需要一个config.json作为配置文件

    Update Notes:
    0x03: 好友功能 + 打歌信息
"""
class Arcaea(object):
    def debug(self):
        return [self.__cred,self.__pswd,self.__auth]
    def __init__(self,path='config.json',precheck = False,byweb = False,**kwargs):
        """<TODO> 把文件读取重写，改为由字典初始化  
        先保留文件读入"""
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
            FakeHeader['AppVersion'] = self._prop.get("AppVer")
        if (self.__auth != None or self.__auth != '') and precheck:
            #WIP
            try: ex = self.getMe()
            except: self.__auth = None
        if self.__auth == None or self.__auth == '':
            if self.__cred is None or self.__pswd is None:
                raise exceptions.badAuthException("Invalid Login Infomation")
            self.__auth = self.getAuth(self.__cred,self.__pswd)
            self._prop['adminAuth'] = self.__auth
            self.__setProp(self.__path)
        else:
            try:
                logging.info("Pre-Testing Auth")
                self.getMe()
            except requests.exceptions.HTTPError as err:
                logging.warning("Auth was Outdated, Reauthing...")
                try: 
                    self.reAuth()
                    self.getMe()
                except:
                    logging.fatal("Bad user cred and pswd, Please Re-check config.json(or your config file)")
                    err.args = ["Bad user cred and pswd, Please Re-check config.json(or your config file)"]
                    raise err
        if precheck:
            data = self.getMe()
            self.user_code = data['user_code']
            self.name = data['user_name']
            
        #pprint(self.Datafetch())
    def __getProp(self,path):
        """
        读取config.json所设置的属性
        """
        with open(path,encoding='UTF-8') as f:
            self._prop = json.load(f)
    def __setProp(self,path):
        """
        写入config.json
        """ 
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
                self.__setProp(self.__path)
        headers = {
              'Authorization': 'Basic ' + b64encode(
                  toencode.encode('ascii')).decode(),
              'DeviceId': deviceid,
              'AppVersion': FakeHeader['AppVersion']}
        po = requests.post(arcauth,headers=headers)
        try:
            po.raise_for_status()
        except requests.exceptions.HTTPError as err:
            err.args = ["Bad user cred and pswd, Please Re-check config.json(or your config file)"]
            raise err
        if po.json()['success']==True: return po.json()['access_token']
        else: raise exceptions.invalidCredException()
        
    def getMe(self):
        """获取个人信息，若无异常返回一个dict对象"""
        headers = self.getHeader({'Authorization':'Bearer '+self.__auth})
        url = arcapi['base'] + arcapi['aggreate'].format(self.generateAggregate(arcapi['me']))
        req = requests.get(url,headers = headers)
        req.raise_for_status()
        return req.json()['value'][0]['value']

    def addFriend(self,friend_code):
        """使用公开的Friend Code(9位)增加好友"""
        friend_code = int(friend_code)
        url = arcapi['base']+arcapi['addFriend']
        headers = self.getHeader({'Authorization':'Bearer '+self.__auth})
        postForm = {"friend_code":friend_code}
        
        req = requests.post(url,headers=headers,data=postForm)
        try:req.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403 or err.response.status_code == 404:
                raise exceptions.FriendError(
                    err,"Friend Error Occured: "
                    +exceptions.friendErrMsg.get(err.response.json()['error_code'],'Unknown Error'))
            else: raise err
        if req.json()['success'] == False: return req.json()
        else: 
            for i in req.json()['value']['friends']:
                if i['user_code'] == str(friend_code): return i
        
    def delFriend(self,friend_id):
        """使用非公开的Friend ID删除好友"""
        friend_id = int(friend_id)
        url = arcapi['base']+arcapi['delFriend']
        headers = self.getHeader({'Authorization':'Bearer '+self.__auth})
        postForm = {"friend_id":friend_id}

        req = requests.post(url,headers=headers,data=postForm)
        try:req.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403 or err.response.status_code == 404:
                raise exceptions.FriendError(
                    err,"Friend Error Occured: "
                    +exceptions.friendErrMsg.get(err.response.json()['error_code'],'Unknown Error'))
            else: raise err
        if req.json()['success'] == True: return True
        else: return False
    
    def reAuth(self):
        self._auth = self.getAuth(self.__cred,self.__pswd)

    def getSongRank(self,song_id,difficulty=2,method = ''):
        """获取特定曲目的信息
        song_id为必填, 将通过查询json文件获取
        难度默认为FTR(2), 其他有PST(0), PRS(1)"""
        assert type (song_id) is str
        assert method in ['', 'me', 'friend']
        url = arcapi['getSongRank{}'.format(method)].format(song_id,difficulty)
        url = arcapi['base']+url
        headers = self.getHeader({'Authorization':'Bearer '+self.__auth})
        req = requests.get(url,headers= headers)
        req.raise_for_status()
        return req.json()['value']

    def __precheck(self,path):
        """前置检查"""
        if not os.path.exists(path): raise OSError("不存在指定配置文件")
        return True

    def getHeader(self,headers):
        """获取HTTP头"""
        assert type(headers) is dict
        ret = (FakeHeader.copy())
        ret.update(headers)
        return ret

    @classmethod
    def generateAggregate(cls,*args, **kwargs):
        """生成endpoint"""
        if len(args) == 0 or args == None: query = ['user/me']
        elif type(args[0]) == str: query = [args[0]]
        else: query = args[0]
        aggregate = '['
        s = 0
        for i in query:
            aggregate = aggregate + '{ "endpoint": "'+i+'", "id": '+str(s)+' }, '
            s+=1
        aggregate = aggregate[:-2]
        aggregate += ']'
        return aggregate
    
    @classmethod
    def initFromFile(cls):
        pass