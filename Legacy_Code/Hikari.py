from . import api,exceptions
import logging,asyncio,requests,threading

class Hikari(api.Arcaea):
    def __init__(self,*args,**kwargs):
        super().__init__()
        # 整一个优先队列出来
        pass
    def __preCheck(self):
        pass
    def _pre_terminate(self):
        pass
    def queryFriendRecent(self,friend_code):
        """通过add/del实现, 按原样返回一个"""

    def queryFriendSongStat(self,songid,difficulty=2):
        """通过 score/song/friend 查询任何人最好成绩"""
        pass
    