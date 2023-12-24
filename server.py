

import json
import asyncio
import logging
import websockets
from datetime import datetime
from aiopath import AsyncPath
from aiofile import async_open
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from main import main as exchange

logging.basicConfig(level=logging.INFO)
LOG_FILE_NAME = "log.csv"

async def file_log(data):
        apath = AsyncPath(LOG_FILE_NAME)
        if  not (await apath.exists() and await apath.is_file()):
            async with async_open(LOG_FILE_NAME, 'w') as file:
                logging.info(f'{LOG_FILE_NAME} creating file')
        async with async_open(LOG_FILE_NAME, 'a') as file:
                await file.write(str(datetime.now()) + " : " +data + "\n")
                logging.info(f'login to file')


async def exchange_task(self, ws, args):
    message = await exchange(args)
    logging.info(f'message tu output = {message}')
    await self.send_to_clients(f"Name {ws.name}: >>>  {message}")


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = datetime.now().time()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            logging.info(f'message tu output = {message}')
            await self.send_to_clients(f"Name {ws.name}: >>>  {message}")

            if "exchange" in message:
                await file_log(message)
                args = (message.split(' '))
                args.append("1") 
                asyncio.create_task(exchange_task(self,ws, args[1:]))
                

async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, '0.0.0.0', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())