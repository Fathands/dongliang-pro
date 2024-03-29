import os
import requests as rq
import execjs
import json
import pandas as pd

# 获取token


def getToken():
    with open(os.path.join(os.path.dirname(__file__), "../hexin-v.js"), "r") as f:
        jscontent = f.read()
    context = execjs.compile(jscontent)
    return context.call("v")


# 获取每页数据


def getPage(**kwargs):
    data = {
        "perpage": 100,
        "page": 1,
        "source": "Ths_iwencai_Xuangu",
        "comp_id": "6623802",
        "uuid": "24087",
        **kwargs,
    }
    res = rq.request(
        method="POST",
        url="http://www.iwencai.com/gateway/urp/v7/landing/getDataList",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        },
    )
    result = json.loads(res.text)
    list = result["answer"]["components"][0]["data"]["datas"]
    return pd.DataFrame.from_dict(list)


# 是否继续循环


def canLoop(loop, count):
    if loop is True:
        return True
    else:
        return count < loop


# 循环分页


def loopPage(loop, **kwargs):
    count = 0
    resultPageLen = 1
    result = None
    if "page" not in kwargs:
        kwargs["page"] = 1
    initPage = kwargs["page"]

    while resultPageLen > 0 and canLoop(loop, count):
        kwargs["page"] = initPage + count
        resultPage = getPage(**kwargs)
        resultPageLen = len(resultPage)
        count = count + 1
        if result is None:
            result = resultPage
        else:
            result = pd.concat([result, resultPage], ignore_index=True)

    return result


# 获取结果


def get(loop=False, **kwargs):
    if loop:
        return loopPage(loop, **kwargs)
    else:
        return getPage(**kwargs)
