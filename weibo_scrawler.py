from tkinter import Listbox

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def weibo_scrawler() -> list:
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://s.weibo.com/top/summary?cate=realtimehot",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
    }
    cookies = {
        "_s_tentry": "passport.weibo.com",
        "Apache": "5513211107437.915.1761372788334",
        "SINAGLOBAL": "5513211107437.915.1761372788334",
        "ULV": "1761372788335:1:1:1:5513211107437.915.1761372788334:",
        "SCF": "Alxqgs_XepYzTNegsfgQpjXD0jwwWK96i6mWeMiGn6bjlr9vUpDNZFcwXJq9DNJhRO1rn30RUhsnc-qmMHh-lJ8.",
        "SUB": "_2A25F-Bt9DeRhGeFL7VMX9CnKzTyIHXVndBK1rDV8PUNbmtANLROgkW9NfctUJomEAFV1ax2_BkbLiDbgcZvVC8Ow",
        "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W58bJ8zrcfwzRkFaBh6euGU5JpX5KzhUgL.FoMfSo2cShMcSo52dJLoI0qLxKnLB.qL1-eLxKqL1KqLBo.LxKML1-2L1hBLxK-LB.-LB--LxK-L12BL1-2LxK-L12qLBoMt",
        "ALF": "02_1763964973"
    }

    url = "https://s.weibo.com/top/summary"
    params = {
        "cate": "realtimehot"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response.close()
    soup = BeautifulSoup(response.text, 'html.parser')
    tr_list = soup.find('div',class_='data').find_all('tr')[1:]
    data_list = []
    for tr in tr_list:
        name = tr.find('td',class_='td-02').find('a').text
        id = tr.find('td',class_='td-02').find('a').get('href')
        link = f'https://s.weibo.com/{id}'
        if 'javascript' not in link:
            print([name, link])
            data_list.append([name, link])
    # df = pd.DataFrame(data_list, columns=["标题","链接"])
    # # 获取当前时间并按指定格式输出
    # formatted_date = datetime.now().strftime("%Y年%m月%d日%H时%M分%S秒")
    # # 保存为 Excel
    # df.to_excel(f"{formatted_date}_微博热搜.xlsx", index=False, engine="openpyxl")
    return data_list