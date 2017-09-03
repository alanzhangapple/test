# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from myapp.models import *

class MybotPipeline(object):

    thr_date = Scrapy_C.objects.all()[0].date
    def process_item(self, item, spider):
        #如果读取的研报发表时间比C表的时间新，则写入数据库，否则认为是旧数据，不保存
        if item["date"]>self.thr_date:
            #如果分析师姓名部分存在逗号，这需要拆分为两条记录
            if "," in item["name"] or "，" in item["name"]:
                
                if "," in item["name"]:
                    tem = ","
                if "，" in item["name"]:
                    tem = "，"

                temp_name_list = item["name"].split(tem)
                for k in temp_name_list:
                    #判断是否为新分析师，如果是新的话，需要在analyst中新建一个分析师对象
                    #print Analyst.objects.filter(name = k,company=item["company"])
                    #print k,item["company"]
                    #os.system("pause")
                    if len(Analyst.objects.filter(name = k,company=item["company"]))==0:

                        Analyst(name = k,company=item["company"]).save()
                    
                    item["name"] = k
                    Scrapy_B(
                                code = item["code"],
                                date = item["date"],
                                title=item["title"],
                                company=item["company"],
                                name = k,
                                content = item["content"],
                            ).save()
            else:
                item.save()
                #判断是否为新分析师，如果是新的话，需要在analyst中新建一个分析师对象
                if len(Analyst.objects.filter(name = item["name"],company=item["company"]))==0:

                    Analyst(name = item["name"],company=item["company"]).save()
        else:
            print "no new article"
        #print "i am here "
        #print spider.parse
    def close_spider(self, spider):
        #爬虫结束之后，先删除C表，然后从B表中查询第一个数据，插入到C表中
        Scrapy_C.objects.all().delete()
        #8.25和8.27,留下8.27，
        t = Scrapy_B.objects.latest("date")
        #插入到C表
        Scrapy_C(
                    code = t.code,
                    date = t.date,
                    title=t.title,
                    company=t.company,
                    name=t.name,
                    content = t.content,
                ).save()
        print "Scrapy_C更新成功！"

