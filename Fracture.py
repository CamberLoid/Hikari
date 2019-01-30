from . import *
import requests,logging,os,sys,json,asyncio
import heapq

class Fracture(Hikari):
    def __init__(self,*args, **kwargs):
        return super().__init__(*args, **kwargs)
