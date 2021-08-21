# 层（LAYER）
YBOT为开发者定义了些许层
## 应用层
应用层处理的是插件，插件的开发可以参考<a href="/API">API</a>和<a href="https://docs.nonebot.dev/">Nonebot</a>
同时，你可以在应用层上新建一个层（衍生层）
## 衍生层
衍生层是由插件内的命令等发起的层，他们会脱离主函数运行
如果你想要让程序在2分钟后执行某个命令，如果使用`await asyncio.sleep(2*60)`，那么，在这期间，如果执行其他命令会导致机器人无法处理，但是，如果你在函数内使用
```python
async def test():
    await asyncio.sleep(2*60)
asyncio.ensure_future(test())
try:
    asyncio.get_event_loop().run_forever()
except AssertionError:
    pass
```
这样就可以成功避免无法处理