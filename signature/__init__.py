# _*_ coding : UTF-8 _*_
# @Time : 2023/11/7 11:19
# @Auther : Tiam
# @File : __init__.py
# @Project : DouyinSpider
import hashlib
import random
import re
import time
from http.cookies import SimpleCookie

import execjs
from urllib.parse import urlparse

import requests
import os


def gen_random_str(random_length):
    """
            根据传入长度产生随机字符串
            """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
    length = len(base_str) - 1
    for _ in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str


class Signature:
    # 这里Cookie指的一提的是msToken可以是随机107位大小写英文字母、数字生成的字符串; 参考: https://github.com/B1gM8c/X-Bogus
    @staticmethod
    def gen_ms_token():
        return gen_random_str(107)

    @staticmethod
    def gen_xbogus(url, user_agent):
        """
        生成X-Bogus, 通过 url 比如 https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&....(其他一大串参数)
        ,和UA生成
        headers 与 cookies 不参与 X-Bogus 生成
        :param url:
        :param user_agent:
        :return:
        """
        # 解析url参数
        query = urlparse(url).query
        # js算法加密生成 X-bogus, 执行js文件中的sign方法
        # os.getcwd() 可以获取当前python程序的工作目录, 使用相对路径是相对的当前工作目录, 并不是相对于当前文件

        path = os.path.dirname(__file__) + '\\X-Bogus.js'
        return execjs.compile(open(path).read()).call('sign', query, user_agent)

    @staticmethod
    def gen_ttwid():
        """
        生成ttwid
        fixme ttwid 的更新频率?
        :return:
        """
        url = 'https://ttwid.bytedance.com/ttwid/union/register/'
        data = {
            "region": "cn",
            "aid": 1768,
            "needFid": False,
            "service": "www.ixigua.com",
            "migrate_info": {"ticket": "", "source": "node"},
            "cbUrlProtocol": "https",
            "union": True
        }
        response = requests.post(url, json=data)
        set_cookie = response.headers['set-cookie']
        # print(set_cookie.split(';'))
        regex = r'ttwid=([^;]+)'
        match = re.search(regex, set_cookie)
        return match.group(1) if match else ''

    @staticmethod
    def gen_access_key(device_id):
        fpId = 9
        appKey = "e1bd35ec9db7b8d846de66ed140b1ad9"
        input_string = f'{fpId}{appKey}{device_id}f8a69f1719916z'
        md5_hash = hashlib.md5()
        md5_hash.update(input_string.encode('utf-8'))
        encrypted = md5_hash.hexdigest()
        # 返回前 32 位并转换为小写
        return encrypted[:32].lower()

    @staticmethod
    def generate_device_id() -> int:
        """
        Generate a spoofed device ID for the TikTok API call

        :return: Device ID number

        """

        return random.randrange(10000000000000000000, 99999999999999999999)

    msToken = 'uFYq9gk5bITk-_XlODxN8Fq6jwE0zKsHB257MfaZ0JIokfIzFVKMf9fe_aniHi0wkZYTAfnnbN5h-YxXr13Yj8miv1v2WL_ig0T2sVVSrhdfiFj55D63JY5D5Fsa-DTGizB0tFaZd86YqbKXjw=='

    @staticmethod
    def gen_tiktok_ms_token():
        headers = {
            'Referer': 'https://www.tiktok.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        params = (
            ('msToken', Signature.msToken),
            # ('X-Bogus', 'DFSzswVOOkVv75VXt55vXZVIVi2p'),
        )

        data = {
            "magic": 538969122,
            "version": 1,
            "dataType": 8,
            "strData": "3Z0GfhRSpkcp/ 18sbGpm1 T0dfamOREsbfGHRbQuBVy0Ow8hFjYX4wgp3pS/90WPviDkpkbu2/UAiw2AzATLvMrtfRplCk7JJdyC0bnbUTedwWd6vAvfMb4EaTggpRYV1et3GzH6uAjYGLYbQmtypWx5Za1tAFbMfZAN5ntFUwLBW09DHDKAPMcE9IzkokuNMoXUDQHRcbTIYTHraLa3R6mjo 9u4Jf9JgRNG76 lssj7JQyi8rPQtX3ogXv86XG6tXOWru6H DFMlNzamKLrQSAFiqBvEd9/jSHL7vKhWiKdEs6cWK6gXO9pgednqSmSLXSFNesI0gRlGQidcg Atyhb2DvRtJZj/TopRLFNydfhKEnlw8Dts5EqfFaNSLlM09h9RkLSur80r1EnC0PSZ3ygiy6ZjTOOhMbLewkNdHf45DIYx3yjHptz7 T8kCQRZslcad3QqxGHiVmOn33crtdeRuo WYq86taSAABcY3 3W9kCsRasdSPzGZ3g5eI260epnewT3 Icyuumgtq8v7nKgesqL/2nvSwUXSUccXAWqanQiyRY/1i0wyGFiIK1lhURTLRT6zVB9fjwhfCugo9g7/7nW6FNHl1YqbP9b2ANhNg23plI5qMEd18igPwRe7WR3kvX8Q5auIcdqXJWKAzRWDGnfFaeFOvjQTQKdK f1F53SPoTn1zmCxGla0BDbEUT2M98Vkw7vDCx1rFriW1uvcPNgfZhRwiSe1TUSbGijZvVfwFz7Eikab4VZ9vqsJ79gdfCdt39q7O0otZrJLcWaQPSryt1SIEXBZwFzaWi5Gz3MAxCs6W2CRqeJzZ7Akaeyko88UxEfROZ6vTCld2BJK34EzqBcGpBVCLpmRnMdr3/pA3BmfNeC23OpXg1qAzz4gjik0aL9jfDAz33K5P9g 5BTClH/dwqHBbS6HCbF/AN/Ty6AYmqEl/SE7V1nbl4eaPsbhe1XV 3rRgnJsLiLTV9oFbCQjRYOeQtGekvAS2KFWmg4piJBk8pwAQLOYKBIO8 66iDeC/UST VTlqLI6M8pvozGv01ODjZZyX 297acxkyu67rlfm0npW8sf3lHaOxWBNolDIj1YVVm9pwbYqLgw16MonQS6eTzzdmk1gbmvcMGi1a1NmlOUwWLZPAAMNAbsef0ypzEKr/geLihSyFxN77K2mR2ehnBu3o8s3ksrgSnC H/OJeaa7xCaqs2Ol0afkRa9owzu8kYU2ubyt3sY lMF/shJW/EPnq9YC6dHeopMBFSX98JIqzVX11iUu9Ch0sqfgXtnQHLXncQDK Ynq8Y5epPe2M1ghWQnbIxBsQpcW47//iFLLi9ZGYqNYY Dx/5tTshPHiRXehxIMpguIzoGboKRr crIM7MWnK/5nbkJE23XQ0q7 2Jamr0xVLhJLSfqTNfmLCFJf3YuuHSi5yV7vkok z54wXqMJBmNvFXvwI7X9emOvr3nc9Cclq4wkg66n/6XjfxKmOSSCyk1Nhy0I060gOYb54wcfbw2rU5IAStO DdNujZ92N2pFHFuGh52I92LUbK wqY8IFiknux/PNPX5mHw/ x4ND7hVsdPvEiy1mEIbgxykx2ojg9 sb1OI9sQ4pAgpY07CNov/rX4FJb86cVrJ8LjUL43hcDORKpovZsXtYY6tzA Bj8YrLaHcHzNZ HwPCOW7dTTTQk20V7 EVlXDohyYhGPW2RX6e7og8IILvLFneSwz2tVpzRQVHFJAxw/YKt1JGlOYtr4VB/7TQalOo76lzCWuMFuEJhJhWo10Vz3Q3oerfgwUbLvLVSuOCHnBz/zk/W3eJ92XNS/uiSStUg0ZawDYl0lEtShDMXF3ze9eh6y1ZAyiLeOcw06 VK3YinmfAi70XQmjVQVFlMb0t8f/R/H/0ZVLJxW326WhK2mEHI8qXcYAaZMgyvGgP0rWYeU8 qMW2DU8G9yfFikSk58mkZW8pRWwIIMYmUndRcS5q3Fxfi/06OyRH4kCGhKUZPl J3Efzl RIvb aVsWeR0aw66TpW9YMEWSuOlU7Sr3ejSD5BmPnlIzb srQ1tJSUgNpwbhiAchQfTn2c2jIY25mlqai7oXxF3OgtSi5Sz58p0FFqg1K AU2RWKdr7DrUMY721jZAiFiu8Zwt3H96rKKW10x/7HzXTfQIMZLn2NdhtRsohEOyyaF/hcRkUcuy1jdaNlMK 8VMh4X/xUXr0DSk ECa4kagi nX/UBC3P6WK6Y/zcb8tbaEtW4Rt7MsRj3tcMkXxOjiWuAx5g3sKn41Z4N3vCdRsJqNS6UqT Hxui0ILM XGBIkp5pKXkUkFdXiTB5GQXTYCZsLMMIQZ2O1jgP6Ruded8FpJFJf6P6xquBWQPQudcLwHTkUQ2hKzvcUx7QCy yhQFrdaF/sHNHY5JJRW3VFajYwDa6JafqyoF4ka2kpjnMOP42cbz3qPCKeVwN5EI2v5j1XLI9JjL EBQUSzRhPd2pGBXoNZfnvQryCEc5auK9THwnf/PrQxSPI8vJ59ZLmW/y9Vq5rfGXyZrQrxM5A61j3k8cgNeB1ryDw54hJJfTVlNWr revHb6OI5CPqeooqA3i9xAtUO8qwMAbdjvIaBrc6dBB3KqwRNjazmBrOYW901mmR91IVwIA9stQI9XGVQg87MSeW3j9FsUdCwdGK8ne2wpnPzoN3p8vW1mj6rDtth6Fk6Jp/0V24sh4U0l4j d7WCs9lb8EByyn6BV3eM9WusBVmmURMRUAP5dEsFbfLYjDff4EXiqXmdCESIG7MoUeoGy5gb/5LuWhYVlq7y8 2cGMpqjnZH T4iFgfVyPoEcLd5pKNx57SlCfyj2yRJ2MnR5n46nW2a3RRC/IJceVlOdhGSLl7chHk8BbpQ5s/WpjvKXWI6wc3Jqm0i7LOS3i2IcB0zMDxWTmU9jQdk5iG4LyKyxCezLYjTh4iUrEIGzNNxpciJ9jl RRU0Z1dZwLfLTHGaSR8osJS520X99u2xPR3u5ISgEm2bGU3B chxwiwNDvhnnvD ZpJoAFTZOuEp5OkpX7fGk2Vpd DunP2I/iCTIP0GHR1oNN7HNCH6SIOfeXyhFlutpsZoV5bi4CDsNrCLgJH0jYNlXepUqb0GAG2DrjBTOOciFRK2NQKIpipjzg8pYqFVZZEHPQ93mWwbbDmhkVN bSXR8VkBD4F9UKsYksPYw7mV9ilRykuUEHi9u0F2 xwcRl/sBebSWUI7uQPZ0HKeRXLPlQSF9dr9rQ IyDI4kLsD2 uvdO6SUmWLEAdVkE3ukrUHjvw3cAsOfg47zpYbmFKodshWfzNC7jQ72NaZd5VVZ0CC5tU3BqIU9Pc03VvKShcs7 BOAAC1odG698Lzi5MYv9KSiFo9MK9JGCMJCXSAxiBBjZ6Oeadwn1Xl r1ed lAhVfS9kPlBMCcJEfnUSZ2WOEsopTWfQPECM/QqRvJDPyif2M3qwrGnJVJYtckowIXNWk00qJTcLaKChZx9rSZUZWuC2rZkEDiwrynf1lqIXS ZheGrau ecJuWw0W0wRJXqCh4Ripr/uE8VUSMqRxqUiyGCgMU0fmhT8OVeWYC1T Wn4EHLmZZYrHN55gfZpwMWT5GHTsvR/tIy2S0oQXdhZhW2 brcqYLpAt2g6yrptzLBD5s/d8YbXhpPWAJsolO7XtKcn7j5LtmB/byvQJgBaN2wu9QFmi8izJaa5bmwAA6QqKvuElL0Q7NeT7AnY1gAEPjYonRuMxIw5UOf7qG6YS5QYkkVlPkS5tmYuxxa1j8AapQFl5qwDXtLDu WmDsbDxcNEc8lZc7nLmge8i6nKhNsBKKrzTWUQYLxG3dnV4srQBMd5oEDEruWne4kkGyw6MehREqNF/QXbTOR3G5M424P/wH1Zx97IvCLgCCmggRO neJ8E': '=",
            "tspFromClient": time.time()
        }

        response = requests.post('https://mssdk-sg.tiktok.com/web/report', headers=headers, params=params, data=data)
        # print(response.status_code)
        jar: SimpleCookie = SimpleCookie()
        jar.load(response.headers['Set-Cookie'])
        Signature.msToken = jar.get('msToken').value
        return Signature.msToken


def test():
    # url = 'https://www.tiktok.com/api/post/item_list/?WebIdLastTime=1711941538&aid=1988&app_language=zh-Hans&app_name=tiktok_web&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%29&channel=tiktok_web&cookie_enabled=true&count=35&coverFormat=2&cursor=0&device_id=7352732694193309214&device_platform=web_pc&focus_state=true&from_page=user&history_len=3&is_fullscreen=false&is_page_visible=true&language=zh-Hans&odinId=7352732794525549599&os=windows&priority_region=&referer=&region=US&screen_height=1440&screen_width=2560&secUid=MS4wLjABAAAA4B_3wIO_nePLe3ZQbVYaldPhA4S8FUOCU25KWLN9jFsaVbIoAyJKYS2ZyqC04YpB&tz_name=Asia%2FShanghai&webcast_language=zh-Hans&msToken=-VZB2FIicKUsZQwIJkSG0YK3a9qgVz-2c5Nn5YS0RF-H_SIWhN46QrfW444VubRT89r2KqQq85I4DaxXFiZjIOy3OV6zc5XTKqW9LOhLN9TAjsGEbvil617HLdmjiTqOylLp15Rezw0F'
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
    # print(Signature.gen_xbogus(url, user_agent))
    # print(Signature.gen_ms_token())
    # print(Signature.gen_ttwid())
    ms_token = Signature.gen_tiktok_ms_token()
    print(ms_token)
    print(len(ms_token))

    print(Signature.gen_tiktok_ms_token())


# print(Signature.gen_access_key('7353551604618855966'))
test()

# 原本的: DFSzswVObPhANnC2t-ClAIS79ddh
# 生成的: DFSzswSLbPhANng1t-ClVU9WcBjn

# 1%7C7bNwGzlfoxFk0M5A0Ga6bI7jLPpBWLVt2SlW9DnTa9g%7C1699288129%7Ce14c38d31876df442429e626286c276072f7a7a7b5ebe8abfe866fba1c3e950e
# 1%7CcBfZs8gcNCYbpScSlcIeCsH8oFRsOi9MAfFrwWd2V18%7C1705382341%7Ca6cff25051a60b433e9b350915b54fd9e0b8fec7d62027d2a04d5048b2650b96
