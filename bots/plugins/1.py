# oding = utf-8
# -*- coding:utf-8 -*-
import random
import time

import requests
from nonebot import on_command, CommandSession
from nonebot.permission import *
from aiocqhttp import MessageSegment
from bot_api.UserApi import *


money_name="YM"


@on_command('sign', aliases=('sign','签到','打卡'),only_to_me=False,permission=EVERYBODY)
async def sign(session: CommandSession):
    execuser_name=str(session.ctx["sender"]["user_id"])
    with open("ct.json","r") as f:
        content=json.load(f)

    state=0

    d=time.strftime("%Y/%m/%d",time.localtime())
    if content["sign"]["data"]!=d:
        content["sign"]["data"]=d
        content["sign"]["people"]=list()
        state = 1
    if execuser_name in content["sign"]["people"]:
        await session.send(MessageSegment.at(int(execuser_name))+"你已经签过到了哦~")
        return

    content["sign"]["people"].append(execuser_name)

    with open("ct.json", "w") as f:
        json.dump(content, f)

    if not (execuser_name in content["users"]):
        create_per(execuser_name)

    #给予经验
    give_jy=random.randint(200,350)
    if state==1:
        give_jy=random.randint(360,420)
    add_jy(give_jy,execuser_name)

    # 给予货币
    give_money = random.randint(200, 350)
    if state == 1:
        give_money = random.randint(360, 420)
    add_money(give_money,execuser_name)




    if state==0:
        await session.send(MessageSegment.at(int(execuser_name))+f"签到成功"+MessageSegment.face(101)+f'\n你获得了{give_jy}经验~，你现在有{get_jy(execuser_name)}经验'+f'\n获得了{give_money}{money_name}~~，你现在有{get_money(execuser_name)}{money_name}'+f"\n今日有{len(content['sign']['people'])}人签到")
    if state==1:
        await session.send(MessageSegment.at(int(execuser_name)) + f"你是今天第一个签到的哦~"+MessageSegment.face(101)+f'\n获得了{give_jy}经验~~，你现在有{get_jy(execuser_name)}经验'+f'\n获得了{give_money}{money_name}~~，你现在有{get_money(execuser_name)}{money_name}')

@on_command('st', aliases=('二刺猿','陈睿叔叔最爱','陈睿叔叔','陈睿',"二次元"),only_to_me=False,permission=EVERYBODY)
async def st(session: CommandSession):
    urldict={
        "https://api.vvhan.com/api/acgimg?type=json":"imgurl",
        "https://api.dongmanxingkong.com/suijitupian/acg/1080p/index.php?return=json":"imgurl",
        "http://api.easys.ltd/api/api/api.php?return=json":"imgurl"
    }
    url=random.choice(list(urldict.keys()))
    url=json.loads(requests.get(url).content.decode("utf-8-sig"))[urldict[url]].strip("/")
    await session.send(MessageSegment.image(url))

@on_command('add_pd', aliases=('添加档案项','添加个人档案项'),only_to_me=False,permission=SUPERUSER)
async def add_pd(session: CommandSession):
    if len(session.event["message"])!=3:
        await session.send("请输入正确的格式")
        return
    get_at_p=session.event["message"][1]["data"]["qq"]
    data=str(session.event["message"][2]).strip()
    add_per_data(get_at_p,data)
    await session.send("成功添加档案项")

@on_command('sub_pd', aliases=('删除档案项','删除个人档案项'),only_to_me=False,permission=SUPERUSER)
async def sub_pd(session: CommandSession):
    if len(session.event["message"])!=3:
        await session.send("请输入正确的格式")
        return
    get_at_p=session.event["message"][1]["data"]["qq"]
    data_num=int(str(session.event["message"][2]).strip())
    ret=sub_per_data(get_at_p,data_num)
    if ret==400:
        await session.send("无法删除档案项，ERROR CODE:400，请检查您的序号是否正确")
        return
    await session.send("成功删除档案项")

@on_command('get_pd', aliases=('查看档案','查看个人档案'),only_to_me=False,permission=SUPERUSER)
async def get_pd(session: CommandSession):
    if len(session.event["message"])!=2:
        await session.send("请输入正确的格式")
        return
    get_at_p=session.event["message"][1]["data"]["qq"]
    t = get_per_data(get_at_p)
    msg = MessageSegment.at(get_at_p) + "该人的档案如下:"
    if len(t)==0:
        msg=MessageSegment.at(get_at_p) + "该人无档案"
        await session.bot.send_group_msg(group_id=session.event["group_id"], message=str(msg))
    for i in range(len(t)):
        msg+="\n"+f"{i}."+t[i]
    await session.bot.send_group_msg(group_id=session.event["group_id"],message=str(msg))

@on_command('cd', aliases=('菜单','menu','帮助','help'),only_to_me=False,permission=EVERYBODY)
async def cd(session: CommandSession):
    await session.send(MessageSegment.text(
"""----------YBOT菜单----------
| 签到 | 打卡 | 二次元 | 陈睿 |
| 天气 | 游戏菜单 | 申请裁决  |
| 

"""
    ))