from django.http import JsonResponse, HttpResponse

import os
import execjs
import json
import requests as rq
import pandas as pd
from . import industry
import datetime

# 获取token


def getToken():
    with open(os.path.join(os.path.dirname(__file__), "../hexin-v.js"), "r") as f:
        jscontent = f.read()
    context = execjs.compile(jscontent)
    return context.call("v")


# 获取每页数据


def getPage(**kwargs):
    data = {"perpage": 100, "page": 1, "source": "Ths_iwencai_Xuangu", **kwargs}
    res = rq.request(
        method="POST",
        url="http://www.iwencai.com/customized/chart/get-robot-data",
        json=data,
        headers={
            "hexin-v": getToken(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        },
    )
    result = json.loads(res.text)
    list = result["data"]["answer"][0]["txt"][0]["content"]["components"][0]["data"][
        "datas"
    ]
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


def get_wencai_data(request):
    now_time = datetime.datetime.now()
    pre_date = (now_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    current_date = now_time.strftime("%Y-%m-%d")

    # 获取前一天df
    pre_df = pd.read_csv("./tables/{}.csv".format(pre_date))

    response_data = {}
    df = get(
        question="20日涨幅从高到底排序的前350只股票；非新股非st；基金持股大于2％的个股或北上资金持股大于0.5％；按行业分类", loop=True
    )
    dongliang_fen_list = []
    for key, value in industry.data.items():
        current_df = df[df["所属同花顺行业"].str.contains("^{}-|-{}-|-{}$".format(key, key, key))][
            ["股票简称", "所属同花顺行业", "最新涨跌幅", "所属概念"]
        ]
        if current_df.empty == False:
            response_data[key] = {}
            response_data[key]["list"] = current_df.to_dict("list")
            response_data[key]["count"] = value
            stock_len = len(response_data[key]["list"]["股票简称"])
            response_data[key]["fenzhi"] = round(stock_len / value * stock_len, 2)
            dongliang_fen_list.append(response_data[key]["fenzhi"])
    industry_names = response_data.keys()
    industry_df_dict = {"板块名称": industry_names, "动量分值": dongliang_fen_list}
    industry_df = pd.DataFrame(industry_df_dict)
    industry_df = industry_df.sort_values(by="动量分值", ascending=False)
    industry_df = industry_df.reset_index(drop=True)
    industry_df["动量排名"] = [x + 1 for x in industry_df.index]

    for x in industry_df["板块名称"]:
        pre_fenzhi = (
            pre_df.loc[pre_df["板块名称"] == x, "动量排名"].iloc[0]
            if (pre_df["板块名称"].eq(str(x))).any()
            else 0
        )
        current_fenzhi = industry_df.loc[industry_df["板块名称"] == x, "动量排名"].iloc[0]
        diff = int(pre_fenzhi) - int(current_fenzhi) if pre_fenzhi != 0 else 0
        industry_df.loc[industry_df["板块名称"] == x, "排名变化"] = int(diff)

    industry_df.to_csv("./tables/{}.csv".format(current_date))

    industry_df.set_index("板块名称")
    result_data = []
    turn_dict = industry_df.T.to_dict()
    for k_index in turn_dict:
        item = {}

        name = turn_dict[k_index]["板块名称"]
        item["key"] = k_index + 1
        item["name"] = name
        item["fenzhi"] = turn_dict[k_index]["动量分值"]
        item["paiming"] = turn_dict[k_index]["动量排名"]
        item["bianhua"] = turn_dict[k_index]["排名变化"]
        temp_list = response_data[name]["list"]
        item["count"] = len(temp_list["股票简称"])
        stock_list = []
        for s_index, stock_name in enumerate(temp_list["股票简称"]):
            stock_item = {}
            stock_item["name"] = stock_name
            stock_item["zhangdie"] = float(temp_list["最新涨跌幅"][s_index])
            gainian = temp_list["所属概念"][s_index]
            stock_item["gainian"] = (
                temp_list["所属概念"][s_index] if isinstance(gainian, str) else ""
            )
            hangye = temp_list["所属同花顺行业"][s_index]
            stock_item["hangye"] = (
                temp_list["所属同花顺行业"][s_index] if isinstance(hangye, str) else ""
            )
            stock_list.append(stock_item)
        stock_list.sort(key=lambda element: element["zhangdie"], reverse=True)
        item["list"] = stock_list
        result_data.append(item)

    result_data = {"data": result_data, "msg": "success"}
    return JsonResponse(result_data, json_dumps_params={"ensure_ascii": False})
