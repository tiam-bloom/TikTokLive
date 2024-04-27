# _*_ coding : UTF-8 _*_
# @Time : 2024/4/27 上午11:37
# @Auther : Tiam
# @File : test_use
# @Project : TikTokLive
# @Desc :
import asyncio

from TikTokLive.client.ws.ws_server import start_websocket_server, message_queue


async def process_receive(data):
    print(data)
    await message_queue.put(data)


async def receive():
    for i in range(10):
        await process_receive(f"{i} 模拟从tiktok直播接收到的消息")
        await asyncio.sleep(1)


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(start_websocket_server())
        tg.create_task(receive())


if __name__ == '__main__':
    asyncio.run(main())
