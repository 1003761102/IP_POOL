import json

from get_requests import get_url
import re
from pyquery import PyQuery as pq

class FreeProxy(object):

    def get_rawproxy(self,callbacks):
        proxies = []
        for callback in callbacks:
            raw_proxy=eval(callback)
            if not raw_proxy==None:
                proxies.append(raw_proxy)
            else:
                print(callback)
        return proxies
    def crawl_181(self):
        start_url = 'http://www.ip181.com/'
        html=get_url(start_url)
        if html:
            ip_adress=re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port,advance in re_ip_adress:
                result = adress + ':' + port
                result=result.replace(' ', '')
                yield result


    def crawl_xicidaili(self):
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(page)
            html = get_url(start_url)
            if html:
                ip_adress = re.compile('<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                # \s* 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(html)
                for adress, port in re_ip_adress:
                    result = adress+':'+ port
                    #print(result)
                    yield result #.replace(' ', '')

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_url(start_url)
            if html:
                ip_adress = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                # \s * 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(html)
                for adress, port in re_ip_adress:
                    result = adress+':'+ port
                    yield result.replace(' ', '')


    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            #print('Crawling', url)
            html = get_url(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])




    def crawl_goubanjia(self):
        start_urls = ['http://www.goubanjia.com/free/gngn/index.shtml','http://www.goubanjia.com/free/gwgn/index.shtml']
        for start_url in start_urls:
            html = get_url(start_url)
            if html:
                doc = pq(html)
                tds = doc('td.ip').items()
                for td in tds:
                    td.find('p').remove()
                    yield td.text().replace(' ', '')
    def crawl_data5u(self):
        for i in ['gngn', 'gwgn']:
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_url(start_url)
            if html:
                ip_adress = re.compile(' <ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>')
                # \s * 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(html)
                for adress, port in re_ip_adress:
                    result = adress+':'+port
                    yield result.replace(' ','')

    def crawl_kxdaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
            html = get_url(start_url)
            if html:
                ip_adress = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
                # \s* 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(html)
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        base_url = 'http://www.kuaidaili.com/free/inha/{}'
        start_urls = [base_url.format(page) for page in range(1, 5)]
        for url in start_urls:
            html = get_url(url)
            if html:
                pattern = '<td data-title="IP">(.*?)</td>\s*?<td data-title="PORT">(.*?)</td>'
                ip_ports = re.findall(pattern, html)
                for ip_port in ip_ports:
                    address = ip_port[0] + ':' + ip_port[1]
                    yield address.replace(' ', '')

    def crawl_xdaili(self):
        start_url = 'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
        html = get_url(start_url)
        if html:
            results = json.loads(html)
            ip_ports = results.get('RESULT').get('rows')
            for ip_port in ip_ports:
                address = ip_port.get('ip') + ':' + ip_port.get('port')
                yield address




