import os
import execjs
import json
import requests as rq
import pandas as pd
import datetime

from django.http import JsonResponse
from . import industry
from utils.wencai import get


def get_all_date(request):
    file_dir = "{}\years".format(os.getcwd())
    result_data = []
    for files in os.listdir(file_dir):
        file_path = "./years/{}".format(files)
        count = 0
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            count = len(df)
        file_name = files.split(".")[0]
        item = {}
        item["date"] = file_name
        item["count"] = count
        result_data.append(item)
    result_data = sorted(result_data, key=lambda item: item["date"], reverse=True)
    result_data = {"data": result_data, "msg": "success"}
    return JsonResponse(result_data, json_dumps_params={"ensure_ascii": False})


def get_years_data(request):
    date = request.GET.get("date")
    df = None
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if str(datetime.date.today()) != str(date):
        file_path = "./years/{}.csv".format(date)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
    else:
        df = get(question="前复权创一年新高股票；所属概念；非新股非st；非北交所；所属行业", loop=True)
        df = df[["股票简称", "所属同花顺行业", "最新涨跌幅", "所属概念"]]
        df["最新涨跌幅"] = pd.to_numeric(df["最新涨跌幅"])
        df = df.sort_values(by="最新涨跌幅", ascending=False)
        df = df.reset_index(drop=True)

        df.set_index("股票简称")
        df.to_csv("./years/{}.csv".format(date))
    result_data = []
    if isinstance(df, pd.DataFrame):
        turn_dict = df.T.to_dict()

        for k_index in turn_dict:
            stock_item = {}
            stock_item["name"] = turn_dict[k_index]["股票简称"]
            stock_item["zhangdie"] = float(turn_dict[k_index]["最新涨跌幅"])
            gainian = turn_dict[k_index]["所属概念"]
            stock_item["gainian"] = (
                turn_dict[k_index]["所属概念"] if isinstance(gainian, str) else ""
            )
            hangye = turn_dict[k_index]["所属同花顺行业"]
            stock_item["hangye"] = (
                turn_dict[k_index]["所属同花顺行业"] if isinstance(hangye, str) else ""
            )
            result_data.append(stock_item)

    result_data = {"data": result_data, "msg": "success"}
    return JsonResponse(result_data, json_dumps_params={"ensure_ascii": False})


def get_wencai_data(request):
    now_time = datetime.datetime.now()
    pre_date = (now_time + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    current_date = now_time.strftime("%Y-%m-%d")

    # 获取前一天df
    pre_file_path = "./tables/{}.csv".format(pre_date)
    pre_df = None
    if os.path.exists(pre_file_path):
        pre_df = pd.read_csv(pre_file_path)

    response_data = {}
    df = get(
        question="20日涨幅从高到底排序的前350只股票；非新股非st；基金持股大于2％的个股或北上资金持股大于0.5％；按行业分类", loop=True
    )
    dongliang_fen_list = []
    for key, value in industry.data.items():
        current_df = df[
            df["所属同花顺行业"].str.contains("^{}-|-{}-|-{}$".format(key, key, key))
        ][["股票简称", "所属同花顺行业", "最新涨跌幅", "所属概念"]]
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
    industry_df = industry_df.sort_values(by=["动量分值", "板块名称"], ascending=False)
    industry_df = industry_df.reset_index(drop=True)
    industry_df["动量排名"] = [x + 1 for x in industry_df.index]

    if pre_df.empty == False:
        for x in industry_df["板块名称"]:
            pre_fenzhi = (
                pre_df.loc[pre_df["板块名称"] == x, "动量排名"].iloc[0]
                if (pre_df["板块名称"].eq(str(x))).any()
                else 0
            )
            current_fenzhi = industry_df.loc[industry_df["板块名称"] == x, "动量排名"].iloc[0]
            diff = int(pre_fenzhi) - int(current_fenzhi) if pre_fenzhi != 0 else 0
            industry_df.loc[industry_df["板块名称"] == x, "排名变化"] = int(diff)
    else:
        industry_df["排名变化"] = ""

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
