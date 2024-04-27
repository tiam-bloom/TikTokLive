# _*_ coding : UTF-8 _*_
# @Time : 2024/4/27 上午10:23
# @Auther : Tiam
# @File : ws_server
# @Project : TikTokLive
# @Desc :
# !/usr/bin/env python
import asyncio

from websockets import WebSocketServerProtocol, serve

# FIFO队列
message_queue = asyncio.Queue()
connected_clients = set()


async def echo(websocket: WebSocketServerProtocol, path: str):
    print(f"Client connected from {websocket.remote_address}", path)
    connected_clients.add(websocket)
    try:
        # await client send a message
        async for message in websocket:
            print(f"Received message from client: {message}")
            while True:
                while message_queue.empty():
                    print("Queue is empty, waiting...")
                    await asyncio.sleep(1)  # 一秒检查一次队列是否为空
                # 获取队列中的消息
                message = await message_queue.get()
                # 广播所有已连接
                for client in connected_clients:
                    # 发送消息给所有已连接的客户端
                    await client.send(message)
                # 发送消息给客户端
                # await websocket.send(message)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 客户端断开连接时移除
        connected_clients.remove(websocket)


async def start_websocket_server():
    print('Starting WebSocket server...')
    async with serve(echo, '0.0.0.0', 8765):
        await asyncio.Future()  # run forever


def main():
    asyncio.run(start_websocket_server())


if __name__ == '__main__':
    main()
