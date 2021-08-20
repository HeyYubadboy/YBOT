#oding = utf-8
# -*- coding:utf-8 -*-
from nonebot import on_request, RequestSession, on_notice, NoticeSession
import nonebot

bot = nonebot.get_bot()  # 在此之前必须已经 init
sid=1806267337

@on_request('friend')
async def auto_add_friend(session: RequestSession):
    await session.bot.set_friend_add_request(flag=session.event['flag'],self_id=sid,approve=True)
    await bot.send_private_msg(user_id=session.event['flag'],message="[YBOT-AUTO] 已自动添加好友",self_id=sid)

@on_request('group')
async def auto_add_group(session: RequestSession):
    await session.bot.set_group_add_request(flag=session.event['flag'],self_id=sid,approve=True,sub_type=session.event['sub_type'])
    await bot.send_group_msg(group_id=session.event['group_id'],message="[YBOT-AUTO] 已自动同意入群",self_id=session.event['self_id'])


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    await session.send('欢迎新朋友～')