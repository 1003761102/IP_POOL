import json
import re

from fake_useragent import UserAgent

from spider import FreeProxy
from get_requests import get_url
import time
from setting import *
from multiprocessing import Process,Pool
import redis
from db import redis_client
import asyncio
import aiohttp
class vaild_check(object):
    def __init__(self):
        self.client=redis_client()
    def check_all_ip(self):
        all_ip = self.client.getall()
        loop = asyncio.get_event_loop()
        tasks = [self.check_one_ip(ip) for ip in all_ip]
        loop.run_until_complete(asyncio.wait(tasks))
    async def check_one_ip(self,ip):
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    UA=UserAgent()
                    base_headers = {
                        'User-Agent': UA.random
                    }
                    if isinstance(ip,bytes):
                        ip=ip.decode('utf-8')
                    proxies = 'http://'+ip
                    print(proxies)
                    # print(base_headers)
                    url = 'http://www.baidu.com'
                    async with session.get(url,proxy=proxies,timeout=5) as response:
                        if response.status==200:
                            self.client.rput(ip)
                            print('successful to proxy************',ip)

                except:

                    print('invaild')
        except:
            print('error')

class addque(object):
    def __init__(self):
        self.client=redis_client()
        self.check=vaild_check()
    def get_proxy(self):
        proxy=FreeProxy()
        callbacks=["self.{name}()".format(name=name) for name in dir(proxy) if 'crawl' in name]
        proxies=proxy.get_rawproxy(callbacks)
        # try:
        loop=asyncio.get_event_loop()
        for web_ip in proxies:
            ips = []
            for ip_port in web_ip:
                # coroutine=self.check.check_one_ip(ip)
                ips.append(ip_port)
            tasks=[self.check.check_one_ip(ip) for ip in ips]
            print('tasks',tasks)
            if tasks:
                loop.run_until_complete(asyncio.wait(tasks))


class schedule(object):
    def check_pool(self):
        que = addque()
        print('check_pool')
        while True:
            conn = que.client.lenth()
            if conn < IPCOUNTS:
                que.get_proxy()
            print('正在等待check_pool')
            time.sleep(15*60)
    def check_pool_chongfu(self):
        while True:
            time.sleep(5*60)
            que=addque()
            print(que.client.lenth())
            que.client.quchong()
            print(que.client.lenth())
            print('等待查重')
            time.sleep(10*60)
    def check_vaild(self):
        while True:
            time.sleep(60*5)
            print('checking_vaild')
            check=vaild_check()
            check.check_all_ip()
            print('等待检查vaild:')
            time.sleep(60*10)
    def run(self):
        vaild=Process(target=self.check_vaild)
        pool = Process(target=self.check_pool)
        chongfu=Process(target=self.check_pool_chongfu)
        pool.start()
        vaild.start()
        vaild.join(5)
        chongfu.start()

