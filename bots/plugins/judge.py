#oding = utf-8
# -*- coding:utf-8 -*-
import asyncio
import time

import nonebot
from nonebot import on_command, CommandSession
from nonebot.permission import *
from aiocqhttp import MessageSegment
from bot_api.UserApi import *

bot = nonebot.get_bot()
sid=2581487884

judge_var={}

@on_command('judge_apply', aliases=('裁决申请','申请裁决'),only_to_me=False,permission=EVERYBODY)
async def judge_apply(session: CommandSession):
    group_count=await session.bot.get_group_info(group_id=session.event["group_id"])
    group_count=group_count['member_count']
    if len(session.event["message"])!=2:
        await session.send(message=MessageSegment.at(session.event['user_id']) + '请输入"裁决申请 类型 @某人"或者"申请裁决 类型 @某人"')
        return
    p1 = str(session.event["message"][0]).split(" ")[1]
    p2 = session.event["message"][1]
    if p2["type"] != "at":
        await session.send(message=MessageSegment.at(session.event['user_id'])+'请输入"裁决申请 类型 @某人"或者"申请裁决 类型 @某人"')
        return
    if str(p2['data']['qq']) in judge_var:
        await session.send(MessageSegment.at(session.event['user_id'])+'该人正在被审')
        return
    if p1=="禁言":
        judge_var[str(p2['data']['qq'])] = {"yes": 0, "no": 0, "class": "禁言",'jy_time':0,'cper':[]}
    elif p1=="踢出":
        judge_var[str(p2['data']['qq'])] = {"yes": 0, "no": 0, "class": "踢出",'cper':[]}
    else:
        await session.send(MessageSegment.at(session.event['user_id']) + "类型只有禁言和踢出")
        return
    if p1=="禁言":
        await session.send(MessageSegment.at(
            session.event['user_id']) + "成功申请裁决\n" + '输入"支持裁决 @被裁决人 希望裁决的分钟数"支持裁决\n' + '输入"反对裁决 @被裁决人"反对裁决\n' + "裁决将在3分钟后判决")
    elif p1=="踢出":
        await session.send(MessageSegment.at(
            session.event['user_id']) + "成功申请裁决\n" + '输入"支持裁决 @被裁决人"支持裁决\n' + '输入"反对裁决 @被裁决人"反对裁决\n' + "裁决将在3分钟后判决")

    async def judge_judge(group_id,judged_per):
        await asyncio.sleep(3*60)
        await bot.send_group_msg(group_id=group_id, message=MessageSegment.at(
            judged_per) + f"的投票结果：支持{judge_var[str(judged_per)]['yes']}票,反对{judge_var[str(judged_per)]['no']}票")
        if not(judge_var[str(judged_per)]['yes']+judge_var[str(judged_per)]['no']>=3):#人数不够，则本案无法审判
            await bot.send_group_msg(group_id=group_id,message=MessageSegment.at(judged_per)+f"的裁决无法进行，因为投票人数过少")
            return
        if judge_var[str(judged_per)]['yes']==judge_var[str(judged_per)]['no']:
            await bot.send_group_msg(group_id=group_id, message=MessageSegment.at(judged_per) + f"的裁决无法进行，因为支持方和反对方票数一致")
            return
        if judge_var[str(judged_per)]['yes']>judge_var[str(judged_per)]['no']:
            pj_time=0
            j_plists_msg="\n案件已加入到此人档案"
            if judge_var[str(judged_per)]['class']=="禁言":
                pj_time=int(judge_var[str(judged_per)]['jy_time']/judge_var[str(judged_per)]['yes'])
                msg=MessageSegment.at(judged_per) + f"的裁决结果是：执行,被禁言{pj_time}分钟"+j_plists_msg
                state=1
            else:
                msg=MessageSegment.at(judged_per) + f"的裁决结果是：执行"+j_plists_msg
                state=0
            await bot.send_group_msg(group_id=group_id, message=msg)
            if state==1:
                await session.bot.set_group_ban(group_id=group_id, user_id=judged_per, duration=pj_time * mj)
            else:
                if judge_var[str(judged_per)]['yes']>=int(group_count/3):
                    await session.bot.set_group_kick(group_id=group_id,user_id=judged_per,reject_add_request=True)
                else:
                    await session.bot.set_group_kick(group_id=group_id, user_id=judged_per)
            add_per_data(judged_per,time.strftime("%Y/%m/%d",time.localtime())+" 被公众投票裁决")
            judge_var.pop(judged_per)
            return


        else:
            await bot.send_group_msg(group_id=group_id, message=MessageSegment.at(judged_per) + f"的裁决结果是：不执行")
            return


    asyncio.ensure_future(judge_judge(session.event['group_id'],str(p2['data']['qq'])))

    try:
        asyncio.get_event_loop().run_forever()
    except AssertionError:
        pass

@on_command('judge_apply_yes', aliases=('支持裁决'), only_to_me=False, permission=EVERYBODY)
async def judge_apply_yes(session: CommandSession):
    at_user=MessageSegment.at(session.event["user_id"])
    if len(session.event["message"]) < 2:
        await session.send(at_user+"请输入正确格式")
        return
    at_p = session.event["message"][1]
    if str(session.event['user_id']) in judge_var[str(at_p['data']['qq'])]['cper']:
        await session.send(at_user+'你已经支持/反对过了哦')
        return
    if not(at_p["data"]['qq'] in judge_var):
        await session.send(at_user+'被裁决人必须已经申请裁决')
        return
    command_tip=at_user+'请输入"支持裁决 @被裁决人"'
    state=0
    if judge_var[str(at_p["data"]["qq"])]["class"]=="禁言":
        command_tip=at_user+'请输入"支持裁决 @被裁决人 希望裁决的分钟数"'
        state=1
        if len(session.event["message"]) != 3:
            await session.send(command_tip)
            return
        p_time = session.event["message"][2]
        if p_time["type"] != "text":
            await session.send(command_tip)
            return
        try:
            p_time = str(p_time)
            p_time = int(p_time)
        except StopAsyncIteration:
            await session.send(at_user+"请输入整数")
            return
        if p_time>600:
            await session.send(at_user+"请输入小于600的数")
            return
    if at_p["type"] != "at":
        await session.send(command_tip)
        return
    if state==1:
        judge_var[str(at_p['data']['qq'])]['yes']+=1
        judge_var[str(at_p['data']['qq'])]["jy_time"]+=p_time
        await session.send(at_user+"成功支持裁决")
    else:
        judge_var[str(at_p['data']['qq'])]['yes'] += 1
        await session.send(at_user+"成功支持裁决")
    judge_var[str(at_p['data']['qq'])]['cper'].append(str(session.event['user_id']))

@on_command('judge_apply_no', aliases=('反对裁决'), only_to_me=False, permission=EVERYBODY)
async def judge_apply_no(session: CommandSession):
    at_user = MessageSegment.at(session.event["user_id"])
    print(session.event["message"])
    if len(session.event["message"]) != 2:
        await session.send(at_user+'请输入"反对裁决 @被裁决人"')
        return
    at_p = session.event["message"][1]
    if not(at_p["data"]['qq'] in judge_var):
        await session.send(at_user+'被裁决人必须已经申请裁决')
        return
    if str(session.event['user_id']) in judge_var[str(at_p['data']['qq'])]['cper']:
        await session.send(at_user+'你已经支持/反对过了哦')
        return
    judge_var[str(at_p['data']['qq'])]['no'] += 1
