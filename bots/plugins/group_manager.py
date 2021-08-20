#oding = utf-8
# -*- coding:utf-8 -*-
from nonebot import on_command, CommandSession
from nonebot.permission import *

mj=60*60

@on_command('ban', aliases=('ban','禁言'),only_to_me=False,permission=SUPERUSER)
async def ban(session: CommandSession):
    try:
        qqn=str(session.get('data', prompt='你想禁言哪个人，请输入Ta的qq号'))
        if len(str(qqn).split(" ")) >= 2:
            await session.send("给爷直接输，别用这招")
            return
        qqn=int(qqn)
    except ValueError:
        await session.send("笑死,你家qq号是这样的？")
        return
    try:
        qqt=int(session.get('data2', prompt='你想禁言那个人的时长(分钟)'))
    except ValueError:
        await session.send("你这是整数？")
        return



    if str(qqn)==str(session.ctx['self_id']):
        await session.send("666，我禁我自己")
        return
    await session.bot.set_group_ban(group_id=session.ctx['group_id'],user_id=qqn,duration=qqt*mj,self_id=session.ctx['self_id'])
    await session.send("成功禁言")


@ban.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['data'] = stripped_arg
        return
    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要禁言的qq号不能为空，请重新输入')
    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg

@ban.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['data2'] = stripped_arg
        return
    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要禁言的时长不能为空，请重新输入')
    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg



@on_command('kick', aliases=('kick','踢出'),only_to_me=False,permission=SUPERUSER)
async def kick(session: CommandSession):
    try:
        qqn=str(session.get('data', prompt='你想移除哪个人，请输入Ta的qq号'))
        if len(str(qqn).split(" ")) >= 2:
            await session.send("给爷直接输，别用这招")
            return
        qqn=int(qqn)
    except ValueError:
        await session.send("笑死,你家qq号是这样的？")
        return


    if str(qqn)==str(session.ctx['self_id']):
        await session.send("666，我踢我自己")
        return
    await session.bot.set_group_kick(group_id=session.ctx['group_id'],user_id=qqn,self_id=session.ctx['self_id'])
    await session.send("成功移除")

@ban.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['data'] = stripped_arg
        return
    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要踢出的qq号不能为空，请重新输入')
    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
