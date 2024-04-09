# _*_ coding : UTF-8 _*_
# @Time : 2024/4/2 10:51
# @Auther : Tiam
# @File : tiktok_live_test
# @Project : TiktokApi
# @Desc :

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, JoinEvent, RoomUserSeqEvent, EnvelopeEvent

# live_addr = input("输入直播地址: ")
live_addr = 'https://www.tiktok.com/@wjq6baodanqifei/live'

unique_id = TikTokLiveClient.parse_unique_id(live_addr)
# Create the client
client: TikTokLiveClient = TikTokLiveClient(unique_id=unique_id)


# Listen to an event with a decorator!
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id}")


@client.on(RoomUserSeqEvent)
async def on_room_user_seq(event: RoomUserSeqEvent):
    print(f'\r当前总人数: {event.total}, 历史总人数: {event.total_user}', end="")


# 监听宝箱
@client.on(EnvelopeEvent)
async def on_envelop(event: EnvelopeEvent):
    print(event)


# Or, add it manually via "client.add_listener()"
# async def on_comment(event: CommentEvent) -> None:
#     print(f"💌{event.user.nickname} -> {event.comment}")
#
#
# client.add_listener(CommentEvent, on_comment)


# @client.on(JoinEvent)
# async def on_join(event: JoinEvent) -> None:
#     print(f'↗️ {event.user.nickname} join')


# client.parse_unique_id()
if __name__ == '__main__':
    client.run()
