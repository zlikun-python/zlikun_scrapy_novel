# -*- coding: utf-8 -*-


import requests
from scrapy.http import HtmlResponse

url = 'https://www.biquge5200.cc/79_79067/148312116.html'
html = requests.get(url).text

response = HtmlResponse(url=url, body=html.encode('gbk'))

title = response.xpath('//div[@class="bookname"]/h1/text()').extract_first().strip()
content = '\r\n'.join(response.xpath('//div[@id="content"]/p/text()').re(r'\S+'))

print(title)
print(content)
