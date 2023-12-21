
import json
import aiohttp
import asyncio
import platform
import datetime
from pprint import pprint



# url = "https://api.privatbank.ua55/p24api/exchange_rates?json&date=01.12.2023"

def make_url(days):
    url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='+str(days.strftime("%d.%m.%Y"))
    return url


async def index(session, url):
    async with session.get(url) as response:
        try:
            # print("Status:", response.status)
            if response.status == 200:
                html = await response.json()
                return html
        except:
            print('exeption')


async def main():
    today = datetime.datetime.now()
    today= today.date()
    days = int(input ("days>>>"))
    res = []
    async with aiohttp.ClientSession() as session:
        try:
            for i in range(days):
                delta = datetime.timedelta(days = i)
                r = await index(session, make_url(today - delta))
                ex = r['exchangeRate']
                for i in ex:
                    if i["currency"] ==  "EUR" :
                        dic = {  r['date'] : {'EUR' : {'sale' : i['saleRate'] , 'purchase' : i['purchaseRate']} , "USD":{}  }   }
                    if i["currency"] ==  "USD" :
                        dic[r['date']]['USD'] = {'sale' : i['saleRate'] , 'purchase' : i['purchaseRate']} 
                        res.append(dic)
            return res
        except aiohttp.client_exceptions.ClientConnectorError: 
            print('bad URL')
        except AssertionError: 
            print('bad URL AssertionError')


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    r = json.dumps(r, indent=2)
    print(r)
    