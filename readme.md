# Arcaea API 自造轮子
**Get yourself lost in the memories in a more *hardcore* way.**

An Unofficial Wrapper for Arcaea/arcapi, named Hikari(Main Branch/High Level API)

单独开了个repo放这个  
本来想离线测试完上线的，结果ssd崩了，丢档，重造，贼不高兴

## DOCs
`api.py`: 底层api, 从Arcaea抓包扒的/`class arcaea(object)`  
`def __init__():`

`Hikari.py`: 包含了一般人用的一些接口和特性什么的/`class Hikari(arcaea):`  

`Fracture.py`: ~~字面, 会导致Bot和你的账号骨折~~ 包含了一些Admin用高级API, 可能会违反ToS所以请不要滥用/`class Fracture(Hikari)`


## TODOs
正在造的:
``` 
master/Hikari -> /me 正在维护的，用途是Telegram上的公用查询
```
之后会开的Branch:
```
Lethe -> /me 计划开发，更多的是个人用途(也就是之前的HikariV1)
Kou -> /me 大概就和Arcapi无关了...以玩梗为主
Fisica -> /offTopic 
#可能理解错了Branch的用法，但是，管他呢
```
---
* 关于config.json  
[ ]todo
* 关于songData.json
[ ]todo

---

基于MIT协议, 作者不对使用产生的后果负责  
Use at your own risk

