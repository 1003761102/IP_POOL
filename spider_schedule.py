import json
import re

from spider import FreeProxy
from get_requests import get_url
import time
from setting import *
from multiprocessing import Process,Pool
import redis
from db import redis_client
class addque(object):
    def __init__(self):
        self.client=redis_client()
    def check_que_ip(self,ip):
        url='http://www.baidu.com'
        # print('异步进行中')
        html=get_url(url,proxy='http://'+ip)
        if html:
            # print('异步成功代理')
            print('successful to proxy************',ip)
            self.client.rput(ip)
    def get_proxy(self):
        proxy=FreeProxy()
        callbacks=["self.{name}()".format(name=name) for name in dir(proxy) if 'crawl' in name]
        proxies=proxy.get_rawproxy(callbacks)
        pool=Pool()
        for web_ip in proxies:
            # print('addque+++++')
            for ip_port in web_ip:
                self.check_que_ip(ip_port)



class vaild_vist(object):
    def __init__(self):
        #self.proxies=FreeProxy()
        self.client=redis_client()
    def check_one_ip(self):
        ip_proxy=self.client.lget()
        url='http://www.baidu.com'
        html=get_url(url,proxy='http://'+ip_proxy)
        if html:
            print('successful to proxy************',ip_proxy)
            self.client.rput(ip_proxy)
    def check_all_ip(self):
        lenth=self.client.lenth()
        for i in range(0,lenth):
             # print('checking_ip_vaild......................')
             self.check_one_ip()
    def check_one_anous(self):
        ip_proxy = self.client.lget()
        url = 'http://api.ipify.org/?format=json'
        html = get_url(url, proxy='http://' + ip_proxy)
        if html:
            try:

                result=json.loads(html)
                print(result)
                ip_checked=result.get('ip')
                print('ip_checked',ip_checked)
                ip_proxy1=re.findall('(.*?):',ip_proxy).pop()
                print('ip_proxy1',ip_proxy1)
                if ip_proxy1==ip_checked:
                    self.client.rput(ip_proxy)
                    print(ip_proxy1,'and',ip_checked)
            except:
                pass
    def check_all_anous(self):
        lenth=self.client.lenth()
        for i in range(0,lenth):
             print('the checkanous lenth is..................................................:',lenth)
             print('checking_ip_anous......................')
             self.check_one_anous()


class schedule(object):
    def check_pool(self):
        que = addque()
        print('check_pool')
        while True:
            conn = que.client.lenth()
            #print(conn)
            if conn < IPCOUNTS:
                que.get_proxy()
            print('正在等待check_pool')
            time.sleep(5*60)
    def check_pool_chongfu(self):
        while True:
            que=addque()
            print(que.client.lenth())
            que.client.quchong()
            print(que.client.lenth())
            time.sleep(600)
    def check_vaild(self):
        while True:
            print('checking_vaild')
            check=vaild_vist()
            check.check_all_ip()
            print('等待检查vaild:')
            time.sleep(600)
    def check_anous(self):
        while True:
            print('checking_anous')
            check=vaild_vist()
            check.check_all_anous()
            print('等待检查anous:')
            time.sleep(600)
    def run(self):
        vaild=Process(target=self.check_vaild)
        pool = Process(target=self.check_pool)
        chongfu=Process(target=self.check_pool_chongfu)
        anous=Process(target=self.check_anous)
        pool.start()
        # pool.join(60)
        chongfu.start()
        vaild.start()
        anous.start()


# que=addque()
# que.get_proxy()
# check=vaild_vist()
# check.check_all_ip()
#check.check_anony_one()

# 检测匿名度Referer:https://www.google.com/
# http://www.xxorg.com/tools/checkproxy/