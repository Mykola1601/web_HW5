
import sys
import json
import aiohttp
import asyncio
import platform
import datetime

def make_url(days):
    url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='+str(days.strftime("%d.%m.%Y"))
    return url


async def index(session, url):
    async with session.get(url) as response:
        try:
            if response.status == 200:
                html = await response.json()
                return html
        except:
            print('exeption')


async def main(days = 1):
    today = datetime.datetime.now()
    today= today.date()
    # days = int(input ("days>>>"))
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
    user_input = 1
    if len(sys.argv) > 1:
        user_input = int(sys.argv[1])
    print(user_input)
    if user_input >= 10:
        print('input 1-10 days')
        exit()
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(user_input))
    r = json.dumps(r, indent=2)
    print(r)
    