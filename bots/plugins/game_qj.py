#oding = utf-8
# -*- coding:utf-8 -*-

import random
import time

from nonebot import on_command, CommandSession
from nonebot.permission import *
from aiocqhttp import MessageSegment
from bot_api.UserApi import *

s_save={}
p_not_jj=get_qj_xf_data()
money_name="YM"



@on_command('qj_with_person', aliases=('跟踪',"尾随"),only_to_me=False,permission=EVERYBODY)
async def qj_with_person(session: CommandSession):
    if not(len(list(session.event["message"]))>=2):
        await session.send(MessageSegment.at(session.event['user_id']) + '请输入"跟踪 @某人"')
        return
    p=session.event["message"][1]
    if p["type"] != "at":
        await session.send(MessageSegment.at(session.event['user_id'])+'请输入"跟踪 @某人"')
        return
    pn=p['data']['qq']
    if pn=="all":
        await session.send(MessageSegment.at(session.event['user_id'])+"别at全体成员啊")
        return
    state=random.choices([1,2,3],weights=[7,3,2])[0]
    if state==1:
        await session.send(MessageSegment.at(session.event['user_id'])+"已成功跟踪，输入强奸 @某人")
        s_save[session.event['user_id']]=[pn,1]
    if state==2:
        await session.send(MessageSegment.at(session.event['user_id'])+"Ta发现你了，把你揍了一顿，住院3分钟")
        await session.bot.set_group_ban(group_id=session.event['group_id'],user_id=session.event['user_id'],duration=3*mj,self_id=session.event['self_id'])
    if state==3:
        await session.send(MessageSegment.at(session.event['user_id'])+"你居然能把人跟没了，然后你发现你背后有警察，你被拘留2分钟，并且记录至档案")
        add_per_data(session.event['user_id'], time.strftime("%Y/%m/%d", time.localtime()) + " 强奸某人")
        await session.bot.set_group_ban(group_id=session.event['group_id'], user_id=session.event['user_id'],
                                        duration=2 * mj, self_id=session.event['self_id'])

@on_command('qj_qj', aliases=('强奸'),only_to_me=False,permission=EVERYBODY)
async def qj_qj(session: CommandSession):
    execuser_name = int(session.ctx["sender"]["user_id"])
    if execuser_name in p_not_jj:
        await session.send(MessageSegment.at(session.event['user_id']) + '鸡鸡都没有，强奸墙角去吧')
        return
    if not(len(list(session.event["message"]))>=2):
        await session.send(MessageSegment.at(session.event['user_id']) + '请输入"强奸 @某人"')
        return
    p = session.event["message"][1]
    if p["type"] != "at":
        await session.send(MessageSegment.at(session.event['user_id']) + '请输入"强奸 @某人"')
        return
    pn = p['data']['qq']
    if pn=="all":
        await session.send(MessageSegment.at(session.event['user_id'])+"你是不是有大病")
        return
    if execuser_name in s_save:
        state = random.choices([1, 2, 3], weights=[6, 2, 2])[0]
        if state == 1:
            add_m=random.randint(300,460)
            add_money(add_m,session.event['user_id'])
            await session.send(MessageSegment.at(session.event['user_id']) + f"已成功强奸{MessageSegment.at(pn)}\n你得到了{add_m}{money_name},现在有{get_money(session.event['user_id'])}{money_name}")
            s_save.pop(session.event['user_id'])
        if state == 2:
            await session.send(MessageSegment.at(session.event['user_id']) + "Ta发现你了，把你揍了一顿，住院3分钟")
            await session.bot.set_group_ban(group_id=session.event['group_id'], user_id=session.event['user_id'],
                                            duration=3 * mj, self_id=session.event['self_id'])
        if state == 3:
            await session.send(MessageSegment.at(session.event['user_id']) + "Ta反客为主，把你的鸡鸡拽下来了")
            add_qj_xf_data(session.event['user_id'])
            p_not_jj=get_qj_xf_data()
    else:
        state = random.choices([1, 2], weights=[2, 8])[0]
        if state==1:
            add_m = random.randint(300, 460)
            add_money(add_m, session.event['user_id'])
            await session.send(MessageSegment.at(session.event[
                                                     'user_id']) + f"已成功强奸{MessageSegment.at(pn)}\n你得到了{add_m}{money_name},现在有{get_money(session.event['user_id'])}{money_name}")
            if session.event['user_id'] in s_save:
                s_save.pop(session.event['user_id'])
        if state==2:
            await session.send(MessageSegment.at(session.event['user_id']) + f"你被拘留了，原因是光天化日直接扑上去强奸{MessageSegment.at(pn)}，并且你的这一行为被记录在了档案里了")
            add_per_data(session.event['user_id'], time.strftime("%Y/%m/%d", time.localtime()) + " 强奸某人")
            await session.bot.set_group_ban(group_id=session.event['group_id'], user_id=session.event['user_id'],
                                            duration=2 * mj, self_id=session.event['self_id'])

@on_command('qj_xf', aliases=('修复鸡鸡'),only_to_me=False,permission=EVERYBODY)
async def qj_xf(session: CommandSession):
    if get_money(session.event["user_id"])>=1200:
        sub_money(1200,session.event['user_id'])
        await session.send(MessageSegment.at(session.event['user_id']) + "成功修复鸡鸡")
    else:
        await session.send(MessageSegment.at(session.event['user_id']) + f"你的{money_name}不足，需要1200{money_name}，你有{get_money(session.event['user_id'])}，快去play you see吧")