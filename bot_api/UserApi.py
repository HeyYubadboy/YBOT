#oding = utf-8
# -*- coding:utf-8 -*-
import json
mj=60*60

def get_content():
    with open("ct.json", 'r') as f:
        return json.load(f)

def create_per(user_num):
    content = get_content()
    user_num = str(user_num)
    content["users"][user_num] = {"lv": 0, "jy": 0, "money": 0,"data":[]}
    with open("ct.json", 'w') as f:
        json.dump(content, f)



def add_money(add_num, user_num):
    content=get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content=get_content()
    content["users"][user_num]["money"] += add_num
    with open("ct.json", 'w') as f:
        json.dump(content, f)


def sub_money(sub_num, user_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content=get_content()
    content["users"][user_num]["money"] -= sub_num
    with open("ct.json", 'w') as f:
        json.dump(content, f)


def get_money(user_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content=get_content()
    return content["users"][user_num]["money"]

def add_jy(add_num, user_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content = get_content()
    content["users"][user_num]["jy"] += add_num
    with open("ct.json", 'w') as f:
        json.dump(content, f)

def get_jy(user_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content = get_content()
    return content["users"][user_num]["jy"]

def add_per_data(user_num,data):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content = get_content()
    content["users"][user_num]["data"].append(data)
    with open("ct.json", 'w') as f:
        json.dump(content, f)

def sub_per_data(user_num,data_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content = get_content()
    if len(content["users"][user_num]["data"]) >= data_num:
        return 400
    content["users"][user_num]["data"].pop(data_num)
    with open("ct.json", 'w') as f:
        json.dump(content, f)

def get_per_data(user_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["users"]):
        create_per(user_num)
        content = get_content()
    return content["users"][user_num]["data"]

def add_qj_xf_data(user_num):
    content = get_content()
    user_num = str(user_num)
    content["p_not_jj"].append(user_num)
    with open("ct.json", 'w') as f:
        json.dump(content, f)

def sub_qj_xf_data(user_num):
    content = get_content()
    user_num = str(user_num)
    if not (user_num in content["p_not_jj"]):
        return 401
    content["p_not_jj"].pop(content["p_not_jj"].index(user_num))
    with open("ct.json", 'w') as f:
        json.dump(content, f)

def get_qj_xf_data():
    content = get_content()
    return content["p_not_jj"]