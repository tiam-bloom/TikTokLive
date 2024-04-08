# _*_ coding : UTF-8 _*_
# @Time : 2024/4/8 9:30
# @Auther : Tiam
# @File : im_fetch_test
# @Project : TikTokLive
# @Desc :
import asyncio

from httpx import Response

from TikTokLive.client.web.web_base import TikTokHTTPClient


async def main():
    web = TikTokHTTPClient()
    web.params['room_id'] = '7355253801794341674'

    response: Response = await web.im_fetch(None)

    print(response.status_code)
    print(response.headers['content-length'])


asyncio.run(main())
