import requests
from fake_useragent import UserAgent
import random
import time
def get_url(url,options={},proxy=None):
    time.sleep(random.random())
    UA=UserAgent()
    base_headers={
        'User-Agent':UA.random,
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    proxies={
        'http':proxy
    }
    headers=dict(base_headers,**options)

    try:
        r=requests.get(url,headers=headers,proxies=proxies,timeout=1)
        r.encoding=r.apparent_encoding

        if r.status_code==200:
            # print(r.status_code)
            return  r.text
        else:
            return None
    except:
        print('Crawling failed',url)
        return None


