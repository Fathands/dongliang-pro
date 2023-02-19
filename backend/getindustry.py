import os
import requests as rq
import execjs
from lxml import etree
import json


def getToken():
    with open(os.path.join(os.path.dirname(__file__), "hexin-v.js"), "r") as f:
        jscontent = f.read()
    context = execjs.compile(jscontent)
    return context.call("v")


def getIndustry():
    data = {}
    # 请求第一页数据
    res = rq.request(
        method="POST",
        url="http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/1/ajax/1/",
        headers={
            "hexin-v": getToken(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        },
    )
    html = res.text
    selector = etree.HTML(html)
    for index in range(1, 51):
        name_list = selector.xpath(
            '//*[@class="m-table m-pager-table"]/tbody/tr[{}]/td[2]/a/text()'.format(
                index
            )
        )
        name = name_list[0]
        up_list = selector.xpath(
            '//*[@class="m-table m-pager-table"]/tbody/tr[{}]/td[7]/text()'.format(
                index
            )
        )
        up_count = up_list[0]
        down_list = selector.xpath(
            '//*[@class="m-table m-pager-table"]/tbody/tr[{}]/td[8]/text()'.format(
                index
            )
        )
        down_count = down_list[0]
        count = int(up_count) + int(down_count)
        if name:
            data[name] = count
    # 请求第二页数据
    res = rq.request(
        method="POST",
        url="http://q.10jqka.com.cn/thshy/index/field/199112/order/desc/page/2/ajax/1/",
        headers={
            "hexin-v": getToken(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        },
    )
    html = res.text
    selector = etree.HTML(html)
    for index in range(1, 27):
        name_list = selector.xpath(
            '//*[@class="m-table m-pager-table"]/tbody/tr[{}]/td[2]/a/text()'.format(
                index
            )
        )
        name = name_list[0]
        up_list = selector.xpath(
            '//*[@class="m-table m-pager-table"]/tbody/tr[{}]/td[7]/text()'.format(
                index
            )
        )
        up_count = up_list[0]
        down_list = selector.xpath(
            '//*[@class="m-table m-pager-table"]/tbody/tr[{}]/td[8]/text()'.format(
                index
            )
        )
        down_count = down_list[0]
        count = int(up_count) + int(down_count)
        if name:
            data[name] = count
    result_text = json.dumps(data, ensure_ascii=False)
    result_text = "data = " + result_text
    print(result_text)
    with open("./main/industry.py", "w", encoding="utf-8") as f:
        f.write(result_text)


getIndustry()
