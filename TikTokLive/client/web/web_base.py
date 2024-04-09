import logging
import os
import random
from abc import ABC, abstractmethod
from typing import Optional, Any, Awaitable, Dict
from urllib.parse import urlencode

import httpx
from httpx import Cookies, AsyncClient, Response, Proxy

from TikTokLive.client.logger import TikTokLiveLogHandler
from TikTokLive.client.web.web_settings import WebDefaults
from signature import Signature


class TikTokHTTPClient:
    """
    HTTP client for interacting with the various APIs

    """

    __uuc: int = 0

    def __init__(
            self,
            proxy: Optional[Proxy] = None,
            httpx_kwargs: dict = {}
    ):
        """
        Create an HTTP client for interacting with the various APIs

        :param proxy: An optional proxy for the HTTP client
        :param httpx_kwargs: Additional httpx k

        """

        self._httpx: AsyncClient = self._create_httpx_client(
            proxy=proxy,
            httpx_kwargs=httpx_kwargs
        )

        self._sign_api_key: Optional[str] = WebDefaults.tiktok_sign_api_key or os.environ.get("SIGN_API_KEY")
        self.__uuc += 1

    def _create_httpx_client(
            self,
            proxy: Optional[Proxy],
            httpx_kwargs: Dict[str, Any]
    ) -> AsyncClient:
        """
        Initialize a new `httpx.AsyncClient`, called internally on object creation

        :param proxy: An optional HTTP proxy to initialize the client with
        :return: An instance of the `httpx.AsyncClient`

        """

        # Create the cookie jar
        self.cookies = httpx_kwargs.pop("cookies", Cookies())

        # Create the headers
        self.headers = {**httpx_kwargs.pop("headers", {}), **WebDefaults.client_headers}

        # Create the params
        self.params: Dict[str, Any] = {
            **httpx_kwargs.pop("params", {}), **WebDefaults.client_params
        }

        return AsyncClient(
            proxies=proxy,
            cookies=self.cookies,
            params=self.params,
            headers=self.headers,
            **httpx_kwargs
        )

    async def im_fetch(self, client):
        # cookies = {
        #     'ttwid': '1%7CX76TLz2ka4LFawrghw22Z2eH76AFtn0Eme207EhpZrM%7C1712228324%7C9ce3aa97b3646d7efef69f9d1cf199d58cd44d37c42483fa18f4ef7c4440056c',
        # }
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'tt_csrf_token=YbRvJOeX-Q3cUBo5vR1h2Q-JUdi-IfjJLd6Q; ak_bmsc=77CC58F2F4567405C23E141361047827~000000000000000000000000000000~YAAQSSw+F3qgf6mOAQAAUQ+rthdfKmQ+9TIguwv0qo57DXF0YJdVg1hoRp216gzEUR5Oxmd+k7hqZeitP5/qTAbK16bdwfstWSXdQ2SzZO0H6yG+ZHSc0/9pBAaHnc4m8Ed4hosKjdJ5BANDzC9fpDBjcolT6L7apLRmIrQokL3f3e7dhGIpYDE6ILqyga+rfntaRdpTpgGsUy6uDkqIkNGHlNnwdeFdMgFpWX7geFGoyBqSKqtfaJjaJY9znpgkBMVRkUO1BlNkaoQLPK1hZV9rJrVqoy4Q1CMWOZoAx8h4d6JKj0b/gqsMRtZZA8hYBfk0EUXx2pm2MY8HFyAFe/OQxsNoaGKt1lUizwqkLdRYvwHJj05whbibm26ZRUKShdnFpdSaALTH; tt_chain_token=AchfTnuD6fSXVgMQjmkyKg==; bm_sv=10E85A894921DD953A1EC3DFC696A8C9~YAAQSSw+F3ugf6mOAQAA1hCrthdy/kMpwvU1NKBmuK/17ilksoDKrO7JuZ5MeBS4XITfINTk7g8eePqVoHzUHdxRMjDhrBpumwbNgy0c7igl1nu7gGxVsQ3O5g7ztHARtsrp0r14kyvKIm7rpTlnI1zp9y//1nByzetY7bEu3UIXtpDACTMLeqBOVhfQ3hG3whhGB4tSFrDVwVtOujjBLDity5itZdpOxVkFuT8vQKrASRN1IaOmvjXpNpBKyUZe~1; odin_tt=ef274707a57631e76cf1746f0deae7d0d72fff9a5d5242d4bd1d153d5e737a78256587a799bdf534db74117929dd64c1e63f76ade8a50bc928ee5740a571e47fe24b71350db11d6ec33da87175aa5c95; passport_csrf_token=6495a8bfa24e04a3199b167acbb3122c; passport_csrf_token_default=6495a8bfa24e04a3199b167acbb3122c; ttwid=1%7CdXcLHA1TVU3hhO97_Rx0SDmIiC702bzMrQOyzhx_PD0%7C1712461669%7Cc3e722ed281d817877dd288a019b5087ce4b00f684ca2e6cc0c1884a84f36d90; csrf_session_id=90ffdfa1bd108902d918ad8b9896fec8; msToken=xc2BuZYGkihRQz_1C2S6a7HlNe1qycYE6Kcv7sr6XPDKn0ocBRJJZGXSstDUnSDW58LczNqcjQHeg7J7jOuxWRfxvsSOfdNbVk0I-AOC5GW_9qAxQPwo1S725k7lXSSV_KR_kgOENfu_fAOAKQ==',
            'origin': 'https://www.tiktok.com',
            'pragma': 'no-cache',
            'referer': 'https://www.tiktok.com/',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        params = (
            ('aid', '1988'),
            ('app_language', 'zh-Hans'),
            ('app_name', 'tiktok_web'),
            ('browser_language', 'zh-CN'),
            ('browser_name', 'Mozilla'),
            ('browser_online', 'true'),
            ('browser_platform', 'Win32'),
            ('browser_version', '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'),
            ('cookie_enabled', 'true'),
            ('cursor', ''),
            ('debug', 'false'),
            ('device_id', ''),
            ('device_platform', 'web'),
            ('did_rule', '3'),
            ('fetch_rule', '1'),
            ('history_comment_count', '6'),
            ('history_comment_cursor', ''),
            ('host', 'https://webcast.us.tiktok.com'),
            ('identity', 'audience'),
            ('internal_ext', ''),
            ('last_rtt', '0'),
            ('live_id', '12'),
            ('resp_content_type', 'protobuf'),
            ('room_id', self.params['room_id']),
            ('screen_height', '1067'),
            ('screen_width', '1707'),
            ('tz_name', 'Asia/Shanghai'),
            ('version_code', '270000'),
            ('msToken', Signature.gen_tiktok_ms_token()),  # '5kBv2_MByq3nd-6WEiPQrMLrV77ExwZYGsTo3b10QBxUakQMc_b9StlpWfXGSWqwuJ-v7lJxGXm4q27cmIJLzwVOPlgU-CivT6z1LYbvFw6CQ7lEsaXcgVZ8yd04l-69OP0zoV1zFyh-az16lA=='
            # ('X-Bogus', 'DFSzswVu73UANHFwt5-34HVIViR-'),
            # ('_signature', '_02B4Z6wo000019P904gAAIDBXdX5ImbGurPT.dcAAJL272'),
        )
        base_url = 'https://webcast.us.tiktok.com/webcast/im/fetch/'
        url = f'{base_url}?{urlencode(params, safe='=')}'.replace('+', '%20')  # URLEncode 中对 空格的编码有 “+”和“%20”两种, 需替换

        x_boys = Signature.gen_xbogus(url, headers.get('user-agent'))
        url += f'&X-Bogus={x_boys}'

        return await (client or self._httpx).get(url, headers=headers)

    async def get_response(
            self,
            url: str,
            extra_params: dict = {},
            extra_headers: dict = {},
            client: Optional[httpx.AsyncClient] = None,
            **kwargs
    ) -> Response:
        """
        Get a response from the underlying `httpx.AsyncClient` client.

        :param url: The URL to request
        :param extra_params: Extra parameters to append to the globals
        :param extra_headers: Extra headers to append to the globals
        :param client: An optional override for the `httpx.AsyncClient` client
        :param kwargs: Optional keywords for the `httpx.AsyncClient.get` method
        :return: An `httpx.Response` object

        """

        # Update UUC param
        self.params["uuc"] = self.__uuc
        self.params["device_id"] = self.generate_device_id()
        if '/webcast/fetch/' in url:
            return await self.im_fetch(client)

        # Make the request
        return await (client or self._httpx).get(
            url=url,
            cookies=self.cookies,
            params={**self.params, **extra_params},
            headers={**self.headers, **extra_headers},
            **kwargs
        )

    async def close(self) -> None:
        """
        Close the HTTP client gracefully

        :return: None

        """

        await self._httpx.aclose()

    def __del__(self) -> None:
        """
        Decrement the UUC on object deletion

        :return: None

        """

        self.__uuc = max(0, self.__uuc - 1)

    def set_session_id(self, session_id: str) -> None:
        """
        Set the session id cookies for the HTTP client and Websocket connection

        :param session_id: The (must be valid) session ID
        :return: None

        """

        self.cookies.set("sessionid", session_id)
        self.cookies.set("sessionid_ss", session_id)
        self.cookies.set("sid_tt", session_id)

    @classmethod
    def generate_device_id(cls) -> int:
        """
        Generate a spoofed device ID for the TikTok API call

        :return: Device ID number

        """

        return random.randrange(10000000000000000000, 99999999999999999999)


class ClientRoute(ABC):
    """
    A callable API route for TikTok

    """

    def __init__(self, web: TikTokHTTPClient):
        """
        Instantiate a route

        :param web: An instance of the HTTP client the route belongs to

        """

        self._web: TikTokHTTPClient = web
        self._logger: logging.Logger = TikTokLiveLogHandler.get_logger()

    @abstractmethod
    def __call__(self, **kwargs: Any) -> Awaitable[Any]:
        """
        Method used for calling the route as a function

        :param kwargs: Arguments to be overridden
        :return: Return to be overridden

        """

        raise NotImplementedError
