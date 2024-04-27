# _*_ coding : UTF-8 _*_
# @Time : 2024/4/27 上午11:21
# @Auther : Tiam
# @File : ws_demo
# @Project : TikTokLive
# @Desc :  https://websockets.readthedocs.io/en/stable/index.html#

import asyncio
import threading

from websockets import WebSocketServerProtocol
from websockets.server import serve
from websockets.sync.client import connect

host = "localhost"
port = 8765


def client():
    with connect(f"ws://{host}:{port}") as websocket:
        websocket.send("Hi")
        while True:
            message = websocket.recv()
            print(f"Received: {message}")


async def echo(websocket: WebSocketServerProtocol, path: str):
    print(f"Client connected from {websocket.remote_address}", path)
    # client send a message
    async for message in websocket:
        for i in range(100):
            await websocket.send(f'{message} {i}')
            await asyncio.sleep(3)


async def main():
    threading.Thread(target=client).start()
    print("Client started")
    async with serve(echo, host, port):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
