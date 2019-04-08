# Arcaea API 自造轮子 / OnDeveloping
**Get yourself lost in the memories in a more *hardcore* way.**

An Unofficial Wrapper for Arcaea/arcapi, named Hikari(Main Branch/High Level API)

~~单独开了个repo放这个~~  
~~本来想离线测试完上线的，结果ssd崩了，丢档，重造，贼不高兴~~  
<TODO>  
2.0.x版本更新了, arcapi的官方版本从4->5, ~~但是我把之前依赖这个写的Bot咕了~~  
总之需要重写了, 顺便把本地啥的整理一下, 就先咕着了  
**0x04 准备**


## DOCs
`api.py`: ~~底层api, 从Arcaea抓包扒的/`class arcaea(object)`  ~~ 计划只会涉及网络IO, 本来是什么都丢在这里了, **计划整理**

`Hikari.py`: 包含了一般人用的一些接口和特性什么的(+上一个版本的api)/`class Hikari(base):`  

`Fracture.py`: ~~字面, 会导致Bot和你的账号骨折~~ 包含了一些Admin用高级API, 可能会违反ToS所以请不要滥用/`class Fracture(Hikari)`


## TODOs
正在造的:
``` 
master/Hikari -> /me 正在维护的，用途是Telegram上的公用查询
```
之后会开的Branch:
```
Lethe -> /me 计划开发，更多的是个人用途(也就是之前的HikariV1)
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

