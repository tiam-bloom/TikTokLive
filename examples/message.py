# _*_ coding : UTF-8 _*_
# @Time : 2024/4/2 10:51
# @Auther : Tiam
# @File : tiktok_live_test
# @Project : TiktokApi
# @Desc :
import asyncio
import json
import logging
import threading
import time

from TikTokLive import TikTokLiveClient

from TikTokLive.client.logger import TikTokLiveLogHandler, LogLevel
from TikTokLive.client.ws import ws_server
from TikTokLive.client.ws.ws_server import start_websocket_server
from TikTokLive.events import ConnectEvent, CommentEvent, JoinEvent, RoomUserSeqEvent, EnvelopeEvent

logger: logging.Logger = TikTokLiveLogHandler.get_logger(level=LogLevel.DEBUG)
# live_addr = input("输入直播地址: ")
live_addr = 'https://www.tiktok.com/@lemmon664/live'

unique_id = TikTokLiveClient.parse_unique_id(live_addr)
# Create the client
client: TikTokLiveClient = TikTokLiveClient(unique_id=unique_id)


# Listen to an event with a decorator!
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id}")


@client.on(RoomUserSeqEvent)
async def on_room_user_seq(event: RoomUserSeqEvent):
    print(f'当前总人数: {event.total}, 历史总人数: {event.total_user}')


# 监听宝箱
@client.on(EnvelopeEvent)
async def on_envelop(event: EnvelopeEvent):
    print(f"宝箱事件! 宝箱ID: {event.envelope_info.envelope_id}, 发送用户ID: {event.envelope_info.send_user_id},  房间ID: {event.common.room_id}")
    # print(json.dumps(event, indent=2, ensure_ascii=False))


# Or, add it manually via "client.add_listener()"
async def on_comment(event: CommentEvent) -> None:
    print(f"💌{event.user.nickname} -> {event.comment}")


client.add_listener(CommentEvent, on_comment)


# @client.on(JoinEvent)
# async def on_join(event: JoinEvent) -> None:
#     print(f'↗️ {event.user.nickname} join')


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(start_websocket_server())
        tg.create_task(client.run())


if __name__ == '__main__':
    # 单独开一个线程, 用户启动转发服务
    threading.Thread(target=ws_server.main).start()
    client.web.set_session_id("0febd4d06773664959ba5dd33ca7bfa7")
    client.run()
