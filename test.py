import json
import re

from get_requests import get_url
def crawl_kuaidaili():
    base_url='http://www.kuaidaili.com/free/inha/{}'
    start_urls=[base_url.format(page) for page in range(1,5)]
    for url in start_urls:
        html=get_url(url)
        if html:
            pattern='<td data-title="IP">(.*?)</td>\s*?<td data-title="PORT">(.*?)</td>'
            ip_ports=re.findall(pattern,html)
            print(ip_ports)
            for ip_port in ip_ports:
                address=ip_port[0]+':'+ip_port[1]
                address.replace(' ','')
                print(address)
def crawl_xdaili():
    start_url='http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10'
    html=get_url(start_url)
    if html:
        results=json.loads(html)
        ip_ports=results.get('RESULT').get('rows')
        for ip_port in ip_ports:
            address=ip_port.get('ip')+':'+ip_port.get('port')
            print(address)
# crawl_kuaidaili()
crawl_xdaili()