# -*- coding:utf-8 -*-

import requests
from db import RedisClient
import json
import time
import random
import re
import asyncio
import aiohttp
from setting import TEST_URL, BATCH_SIZE, VALID_STATUS_CODES
import sys

class Tester():
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        """
        # 如果proxy是字节类型的，以utf-8格式解码
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        real_proxy = 'http://' + proxy
        # 不验证SSL
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # 访问httpbin
                async with session.get(TEST_URL, proxy=real_proxy, timeout=7, allow_redirects=False) as req:
                    # # 获取相应内容
                    # response_content = await req.json()
                    # ip_response = response_content['origin']
                    # # 获取访问IP
                    # juege_proxy = re.search('(.*):', proxy).group(1)
                    # # 判断访问IP是否与代理一致
                    # if ip_response == juege_proxy:
                    #     # 代理分值设置为最高
                    #     self.redis.max(proxy)
                    #     # print('代理可用', proxy)
                    if req.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)

            except Exception as e:
                # print(e.args)
                # 有异常则代理分数减一
                self.redis.decrease(proxy)
                # print('代理不可用，分值-1', proxy)

    def run(self):
        """
        批量测试代理
        """
        try:
            # 获取当前代理池代理数量
            count = self.redis.count()
            print('当前共有', count, '个代理!')
            # 批量测试代理
            for i in range(0, count, BATCH_SIZE):
                start = i
                stop = min(i + BATCH_SIZE, count-1)
                print('正在测试第', start+1, '-', stop, '个代理！')
                proxies_list = self.redis.batch(start, stop)
                # 启用一个事件循环
                loop = asyncio.get_event_loop()
                # 把携程对象封装为task
                task = [self.test_single_proxy(proxy) for proxy in proxies_list]
                # 运行
                loop.run_until_complete(asyncio.wait(task))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
            
def main():
    mytester = Tester()
    mytester.run()

if __name__ == '__main__':
    main()