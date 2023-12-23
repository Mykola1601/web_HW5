
import sys
import json
import aiohttp
import asyncio
import logging
import platform
import datetime

logging.basicConfig(level=logging.INFO)

# valutes= ["EUR","USD"]

def make_url(days):
    url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='+str(days.strftime("%d.%m.%Y"))
    logging.info(f'url = {url}')
    return url


async def index(session, url):
    async with session.get(url) as response:
        try:
            logging.info(f'response.status == {response.status } ')
            if response.status == 200:
                html = await response.json()
                return html
        except:
            logging.info(f'exeption in index response ')


async def main(args):
    logging.info(f'incomin args = {args}')
    days = "1"
    valutes= ["EUR","USD"]
    if len(args) >0:
        days = args[0]
        valutes.extend(args)
    if not days.isdigit():
        return 'wrong number of days'
    if int(days) > 10:
        return 'to mach days >>> 1-10'
    days = int(days)
    today = datetime.datetime.now()
    today= today.date()
    logging.info(f'incomin days = {days}')
    logging.info(f'valutes = {valutes}')
    res = []

    async with aiohttp.ClientSession() as session:
        try:
            for i in range(days):
                delta = datetime.timedelta(days = i)
                r = await index(session, make_url(today - delta))
                dic = {  r['date'] : {}   }
                ex = r['exchangeRate']
                for i in ex:
                    if i["currency"] in valutes :
                        dic[r['date']].update({i["currency"] : {'sale' : i['saleRateNB'] , 'purchase' : i['purchaseRateNB']} })
                res.append(dic)
            logging.info(f'respons finish ')    
            return res
        except aiohttp.client_exceptions.ClientConnectorError: 
            logging.info(f'except == {aiohttp.client_exceptions.ClientConnectorError} ')
        except AssertionError: 
            logging.info(f'except == {AssertionError} ')


if __name__ == "__main__":
    logging.info(f'main == __name__')
    logging.info(f'input args = {sys.argv}')
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(sys.argv[1:]))
    r = json.dumps(r, indent=2)
    print(r)



