import platform

import aiohttp
import asyncio
import requests

response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2023')
exchange_rate = response.json()
print(exchange_rate)
response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=02.12.2023')
exchange_rate = response.json()
print(exchange_rate)
# response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=03.12.2023')
# exchange_rate = response.json()
# print(exchange_rate)
# response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=04.12.2023')
# exchange_rate = response.json()
# print(exchange_rate)
# response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=05.12.2023')
# exchange_rate = response.json()
# print(exchange_rate)
# response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=06.12.2023')
# exchange_rate = response.json()
# print(exchange_rate)