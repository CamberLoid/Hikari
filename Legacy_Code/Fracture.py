from . import api, Hikari, exceptions
import requests,logging,os,sys,json,asyncio
import heapq

class Fracture(Hikari.Hikari):
    def __init__(self,*args, **kwargs):
        return super().__init__()
