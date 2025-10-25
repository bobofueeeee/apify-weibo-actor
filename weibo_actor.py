"""Module defines the main entry point for the Apify Actor."""

from __future__ import annotations

from apify import Actor
from bs4 import BeautifulSoup
from httpx import AsyncClient
import asyncio


async def fetch_weibo_hot_search() -> list[dict]:
    """Fetch Weibo real-time hot search data."""
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
    params = {"cate": "realtimehot"}

    async with AsyncClient() as client:
        Actor.log.info('Fetching Weibo hot search data...')
        response = await client.get(url, headers=headers, cookies=cookies, params=params, follow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')

        tr_list = soup.find('div', class_='data').find_all('tr')[1:]
        data_list = []

        for tr in tr_list:
            name = tr.find('td', class_='td-02').find('a').text.strip()
            id = tr.find('td', class_='td-02').find('a').get('href')
            link = f'https://s.weibo.com/{id}'

            if 'javascript' not in link:
                Actor.log.info(f'Extracted hot search: {name} - {link}')
                data_list.append({
                    'title': name,
                    'url': link,
                    'source': 'weibo_hot_search',
                    'timestamp': asyncio.get_event_loop().time()  # Using event loop time as timestamp
                })

        print("return data_list")

        return data_list


async def main() -> None:
    """Main entry point for the Apify Actor."""
    async with Actor:
        # Get Actor input
        actor_input = await Actor.get_input() or {}

        # Optionally process the input URL if needed
        url = actor_input.get('url', 'https://apify.com/')

        # Fetch Weibo hot search data
        weibo_data = await fetch_weibo_hot_search()

        print("actor push weibo data")

        # Save to dataset
        await Actor.push_data(weibo_data)

        # Optional: Process the input URL (original functionality)
        # if actor_input.get('process_url', False):
        #     async with AsyncClient() as client:
        #         Actor.log.info(f'Sending a request to {url}')
        #         response = await client.get(url, follow_redirects=True)
        #
        #     soup = BeautifulSoup(response.content, 'lxml')
        #     headings = []
        #
        #     for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        #         heading_object = {
        #             'level': heading.name,
        #             'text': heading.text.strip(),
        #             'source': 'page_content'
        #         }
        #         Actor.log.info(f'Extracted heading: {heading_object}')
        #         headings.append(heading_object)
        #
        #     if headings:
        #         await Actor.push_data(headings)



# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())