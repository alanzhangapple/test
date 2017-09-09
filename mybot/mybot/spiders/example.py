# -*- coding: utf-8 -*-
import scrapy
import urllib2
from lxml import etree
from scrapy.spider import BaseSpider
from mybot.items import PersonItem
import sys
import os
from mybot.items import Scrapy_B_Item
from mybot.items import AnalystItem
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

#生成6000个页面
start_url = ['http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/company/index.phtml']
first_url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/company/index.phtml?p='
for i in range(1,2000):
    start_url.append(first_url+str(i))

class ExampleSpider(BaseSpider):
    name = 'example'
    #allowed_domains = ['example.com']
    start_urls = start_url
    
    def start_requests(self):
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        
        for quote in response.css('td.f14 a::attr("href")'):
            next_page = quote.extract()
            if next_page is not None:
                item = Scrapy_B_Item()
                request=urllib2.Request(next_page)
                request.add_header("user-agent","Mozilla/5.0")#伪装成浏览器
                res_cont=urllib2.urlopen(request,timeout=10)
                tree = etree.HTML(res_cont.read().decode('gb2312', 'ignore'))
                
                #录入股票代码
                if tree.xpath('//div[@id="stocks"]/table/tbody/tr/td[1]/text()')!=[]:
                    item["code"] = tree.xpath('//div[@id="stocks"]/table/tbody/tr/td[1]/text()')[0]
                #录入调研员时间
                if tree.xpath('//div[@class="creab"]/span[4]/text()')!=[]:
                    date_str = tree.xpath('//div[@class="creab"]/span[4]/text()')[0].replace("日期：","")
                    item["date"] = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                #禄蠹调研标题
                if tree.xpath('//div[@class="content"]/h1/text()')!=[]:
                    item["title"] = tree.xpath('//div[@class="content"]/h1/text()')[0]
                
                if tree.xpath('//div[@class="creab"]/span/a/text()')!=[]:
                    #录入调研公司
                    item["company"] = tree.xpath('//div[@class="creab"]/span/a/text()')[0]
                    #录入调研分析师姓名
                    item["name"] = tree.xpath('//div[@class="creab"]/span/a/text()')[1]
                    
                    
                #录入研究报告的内容
                if tree.xpath('//div[@class="blk_container"]/p/text()')!=[]:
                    #print tree.xpath('//div[@class="blk_container"]')
                    #item["content"] = tree.xpath('//div[@class="blk_container"]').xpath("string(.)").exttract()[0]
                    item["content"] = tree.xpath('//div[@class="blk_container"]')[0].xpath('string(.)').strip()
                 
                #yield response.follow(next_page, self.parse)
                #return item
                yield item

