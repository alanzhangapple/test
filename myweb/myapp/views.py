# -*- coding: utf-8 -*-
from django.shortcuts import render
import tushare as ts
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from sqlalchemy import create_engine
from myapp.models import *
from datetime import timedelta
import time
from django.db.models import Avg
# Create your views here.
import os
import xlwt
import platform
import traceback
import csv
#判断操作系统
#如果是windows系统，就用'r'sqlite:///E:\test\myweb\db\myweb.db''
#如果是ubuntu，就用"r'sqlite:////test/myweb/db/myweb.db"
sysstr = platform.system()
if(sysstr =="Windows"):
#print ("Call Windows tasks")
    db_path = r'sqlite:///E:\test\myweb\db\myweb.db'
elif(sysstr == "Linux"):
#print ("Call Linux tasks")
    db_path = r'sqlite:////test/myweb/db/myweb.db'
else:
#print ("Other System tasks")
    db_path = r'sqlite:////test/myweb/db/myweb.db'

def stock_base_view(request):
    
    #获取数据库操作引擎
    #1. 更新股票档案数据库
    #2. 更细股票每天的涨跌幅数据
    engine = create_engine(db_path)
    df = ts.get_stock_basics()
    
    #先清空数据，然后再添加
    #print Stock_base.objects.all().count()
    Stock_base.objects.all().delete()
    df.to_sql('myapp_stock_base',engine,if_exists='append')
    #df.to_sql('myapp_stock_base_test',engine)
    result_message = "添加成功！"
    return HttpResponse(result_message)
    


def Analyst_power_today_view(request):
    #localhost:8080/Analyst_power_today
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    Analyst_power_today.objects.all().delete()#先删除掉所有记录
    #统计每个分析师在每个周期的平均涨跌幅，30天，60天，90天，180天
    for k in Analyst.objects.all():
        t = Scrapy_D.objects.filter(name = k.name,boolean_str=1)
        #print t
        if t:
            Analyst_power_today(
                                name = t[0].name,
                                company = t[0].company,
                                
                                power_30 = t.aggregate(Avg('charge_delta_30_date'))["charge_delta_30_date__avg"],
                                power_30_high = t.aggregate(Avg('hightest_price_delta_30_date'))["hightest_price_delta_30_date__avg"],
                                
                                power_60 = t.aggregate(Avg('charge_delta_60_date'))["charge_delta_60_date__avg"],
                                power_60_high = t.aggregate(Avg('hightest_price_delta_60_date'))["hightest_price_delta_60_date__avg"],
                                
                                power_90 = t.aggregate(Avg('charge_delta_90_date'))["charge_delta_90_date__avg"],
                                power_90_high = t.aggregate(Avg('hightest_price_delta_90_date'))["hightest_price_delta_90_date__avg"],
                                
                                power_180 = t.aggregate(Avg('charge_delta_180_date'))["charge_delta_180_date__avg"],
                                power_180_high = t.aggregate(Avg('hightest_price_delta_180_date'))["hightest_price_delta_180_date__avg"],
                                
                                ).save()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+"\n"+start_time+"\n"+"结束时间："+end_time
    return HttpResponse(result_message)
    
def Analyst_power_history_view(request):
    #将当前的分析师能力数据保存到数据库，留作备份历史数据
    #localhost:8080/Analyst_power_history
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    date_now = datetime.datetime.now()
    for k in Analyst_power_today.objects.all():
        Analyst_power_history(
                                name = k.name,
                                company = k.company,
                                
                                power_30 =  k.power_30,
                                power_60 =  k.power_60,
                                power_90 =  k.power_90,
                                power_180 = k.power_180,
                                date = date_now,
                                ).save()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
def duz(a,b):
    if a==0 or b==0:
        return 0
    else:
        return float(a/b-1)

def if_hot(need_price_data,code):
    #判断是否为一字板涨停股票
    #一字板的表准是：open=close=high=low

    for i in need_price_data:
        if i["code"]== code and i["open"]==i["high"] and i["close"]==i["open"] and i["open"]==i["low"]:
            return 0
        else:
            return 1

        
def max_price(need_price_data,code,publish_date,delta):
    #计算时间间隔内股票的最高价格，如30天以内，最高的价格
    
    last_date = publish_date + timedelta(days = delta)
    date_publish_weekday = last_date.weekday()
    price_data =[0]
    #如果遇到周六周日，统一记作周五
    if date_publish_weekday == 6:
        last_date = last_date-datetime.timedelta(days = 2 )

    if date_publish_weekday == 5:
        last_date = last_date-datetime.timedelta(days = 1 )
    
    #这里遍历时间太久了，不能完全遍历，此处需要增加一个开关，如果增加了足够的数据，就跳出循环
    #delta表示需要增加的数据数量
    
    for i in need_price_data:
        #if i["code"]== code and i["date"] >= publish_date.strftime("%Y-%m-%d")  and i["date"] <= last_date.strftime("%Y-%m-%d"):
        if i["code"]== code and i["date"] >= publish_date.strftime("%Y-%m-%d"):#
            price_data.append(i["close"])
            if len(price_data) == delta:
                return max(price_data)
                

    return max(price_data)
    
def get_price(i,code,last_date):
    #print "in",code,last_date
    price_data = 0
    #os.system("pause")
    if i["code"]== code and i["date"]==last_date.strftime("%Y-%m-%d"):
        price_data = i["close"]
        #print "in in"
        return price_data
    return price_data
    
def comupter_delta(need_price_data,code,publish_date,delta):
    #计算间隔时间的股票价格，如30天之后的价格
    #input：股票编码合并数据，股票编码，发布时间，延迟时间
    #output:价格，此处价格为收盘价

    price_data = 0
    last_date = publish_date + timedelta(days = delta)
    date_publish_weekday = last_date.weekday()
    #如果遇到周六周日，统一记作周五
    if date_publish_weekday == 6:
        last_date = last_date-datetime.timedelta(days = 2 )

    if date_publish_weekday == 5:
        last_date = last_date-datetime.timedelta(days = 1 )
    #如果查不到股票价格，价格就是0


    for i in need_price_data:
        if i["code"]== code and i["date"]==last_date.strftime("%Y-%m-%d"):
            price_data = i["close"]
            return price_data
    return price_data

    
def write_content(k):
    if u"买入" in k.content or u"增持" in k.content:
        if_computer = 1
    else:
        if_computer = 0
    
    
    Scrapy_D(
                code = k.code,
                date = k.date,
                title = k.title,
                company = k.company,
                name = k.name,
                content = k.content,
                boolean_str = if_computer,
                
                price_publish_date = 0,#从发布日期往后推0天的价格
                
                delta_30_date = k.date + timedelta(days = 30),
                price_delta_30_date = 0,#从发布日期往后推30天
                charge_delta_30_date = 0, #30天后涨跌幅
                hightest_price_delta_30_date=0,#30天后最高涨跌幅
                
                delta_60_date = k.date + timedelta(days = 60),
                price_delta_60_date = 0,#从发布日期往后推60天
                charge_delta_60_date = 0,#60天后涨跌幅
                hightest_price_delta_60_date=0,#60天后最高涨跌幅
                
                delta_90_date = k.date + timedelta(days = 90),
                price_delta_90_date = 0,#从发布日期往后推90天
                charge_delta_90_date = 0,#90天后涨跌幅
                hightest_price_delta_90_date=0,#90天后最高涨跌幅
                
                
                delta_180_date = k.date + timedelta(days = 180),
                price_delta_180_date = 0,#从发布日期往后推180天
                charge_delta_180_date =0,#180天后涨跌幅
                hightest_price_delta_180_date=0,#180天后最高涨跌幅
            ).save()
def ArticleComputer_view(request):
    #localhost:8080/ArticleComputer
    #获取研报中每条数据的价格，发布价格、30天后价格、60天后价格、90天后价格
    #将Scrapy_B 表中今天的数据，逐个从CSH_price中查询到交易数据之后，增加到Scrapy_D表中
    #today_data = datetime.datetime.now() #today_data.strftime("%Y-%m-%d")
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #1.先将Scrapy_B 中的数据补充到Scrapy_D的表中
    #2.再更新Scrapy_D中，30，60，90，180为空的数据
    
    
    #优化查询，由于CHS_price数据有400W条，因此只查询一次
    Scrapy_B_title_list = Scrapy_B.objects.all().values_list("title",flat=True)
    
    #查询所有需要插入的价格，先看是否有相同数据，有的话则删除
    t = Scrapy_D.objects.filter(title__in = Scrapy_B_title_list)

    t.delete()
    print "strat",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    map(write_content,Scrapy_B.objects.all())

    #更新Sccrapy_D表中，发布日期、30天后、60天后、90天后、180天后为空的数据
    
    #从CHS_price中查询一次所有的数据
    #print "A",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    '''
    Scrapy_B_code_list = Scrapy_B.objects.all().values_list("code",flat=True)
    #print "time 1:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    need_price_data  = CSH_price.objects.filter(code__in = Scrapy_B_code_list).values("code","date","close")
    for i in Scrapy_D.objects.filter(price_publish_date = 0):
        i.price_publish_date = comupter_delta(need_price_data,i.code,i.date,0)#更新发布时的价格
        i.save()
    print "B",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    for i in Scrapy_D.objects.filter(price_delta_30_date = 0):
        i.price_delta_30_date = comupter_delta(need_price_data,i.code,i.date,30)#更新30天后的价格
        i.charge_delta_30_date = duz(comupter_delta(need_price_data,i.code,i.date,30),i.price_publish_date)#更新30天后的涨跌幅
        i.hightest_price_delta_30_date  = duz(max_price(need_price_data,i.code,i.date,30),i.price_publish_date)#更新30天后的最高涨幅
        #i.hightest_price_delta_30_date  = max_price(need_price_data,i.code,i.date,30)#更新30天后的最高价格
        i.save()
    print "C",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    for i in Scrapy_D.objects.filter(price_delta_60_date = 0):
        i.price_delta_60_date = comupter_delta(need_price_data,i.code,i.date,60)#更新60天后的价格
        i.charge_delta_60_date = duz(comupter_delta(need_price_data,i.code,i.date,60),i.price_publish_date)#更新60天后的涨跌幅
        i.hightest_price_delta_60_date  = duz(max_price(need_price_data,i.code,i.date,60),i.price_publish_date)#更新30天后的最高涨幅
        i.save()
    print "D",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    for i in Scrapy_D.objects.filter(price_delta_90_date = 0):
        i.price_delta_90_date = comupter_delta(need_price_data,i.code,i.date,90)#更新90天后的价格
        i.charge_delta_90_date = duz(comupter_delta(need_price_data,i.code,i.date,90),i.price_publish_date)#更新90天后的涨跌幅
        i.hightest_price_delta_90_date  = duz(max_price(need_price_data,i.code,i.date,90),i.price_publish_date)#更新90天后的最高涨幅
        i.save()
    print "E",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    for i in Scrapy_D.objects.filter(price_delta_180_date = 0):
        i.price_delta_180_date = comupter_delta(need_price_data,i.code,i.date,180)#更新180天后的价格
        i.charge_delta_180_date = duz(comupter_delta(need_price_data,i.code,i.date,180),i.price_publish_date)#更新180天后的涨跌幅
        i.hightest_price_delta_180_date  = duz(max_price(need_price_data,i.code,i.date,180),i.price_publish_date)#更新180天后的最高涨幅
        i.save()
    print "F",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #遍历Scrapy_D,如果是一字板的话，就不参与计算
    #一字板的表准是：open=close=high=low
    for i in Scrapy_D.objects.filter(boolean_str = 1):
        #判断是否为一字板涨停股票，是的话，不参与计算
        t =if_hot(need_price_data,k.code)
        if not t:
            i.boolean_str = t
            i.save()
    '''
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)

#从CHS_price中查询一次所有的数据
#date_now = datetime.datetime.now()-timedelta(days = 365)#往前推1年
strt = '2016-1-1'
date_time = datetime.datetime.strptime(strt,'%Y-%m-%d')
Scrapy_B_code_list = Scrapy_B.objects.filter(date__gt = date_time).values_list("code",flat=True)
#print "time 1:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))查询2016年的股票
need_price_data  = CSH_price.objects.filter(code__in = Scrapy_B_code_list).values("code","date","close")
stock_base_data = Stock_base.objects.filter(code__in = Scrapy_B_code_list).values("code","timeToMarket")
def  computer_30(i):
    #print "i am here"
    i.price_delta_30_date = comupter_delta(need_price_data,i.code,i.date,30)#更新30天后的价格
    i.charge_delta_30_date = duz(comupter_delta(need_price_data,i.code,i.date,30),i.price_publish_date)#更新30天后的涨跌幅
    i.hightest_price_delta_30_date  = duz(max_price(need_price_data,i.code,i.date,30),i.price_publish_date)#更新30天后的最高涨幅
    try:
        i.save()
    except Exception as e:
        print "yichang!!!"
        record_except()
        record_log(i.code)
        record_log(i.date)


    
    
def ArticleComputer_2_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "start",start_time
    #查询ScrapyD表中数据30天为0的数据,先计算2016年至今的数据
    k = Scrapy_D.objects.filter(price_delta_30_date = 0,date__gt = date_time)
    map(computer_30,k)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)

    
    
def  computer_60(i):
    #print "i am here"
    i.price_delta_60_date = comupter_delta(need_price_data,i.code,i.date,60)#更新60天后的价格
    i.charge_delta_60_date = duz(comupter_delta(need_price_data,i.code,i.date,60),i.price_publish_date)#更新60天后的涨跌幅
    i.hightest_price_delta_60_date  = duz(max_price(need_price_data,i.code,i.date,60),i.price_publish_date)#更新60天后的最高涨幅
    try:
        i.save()
    except Exception as e:
        print "yichang!!!"
        record_except()
        record_log(i.code)
        record_log(i.date)


    
    
def ArticleComputer_3_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "start",start_time
    #查询ScrapyD表中数据60天为0的数据,先计算2016年至今的数据
    k = Scrapy_D.objects.filter(price_delta_60_date = 0,date__gt = date_time)
    map(computer_60,k)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
def  computer_90(i):
    #print "i am here"
    i.price_delta_90_date = comupter_delta(need_price_data,i.code,i.date,90)#更新90天后的价格
    i.charge_delta_90_date = duz(comupter_delta(need_price_data,i.code,i.date,90),i.price_publish_date)#更新90天后的涨跌幅
    i.hightest_price_delta_90_date  = duz(max_price(need_price_data,i.code,i.date,90),i.price_publish_date)#更新90天后的最高涨幅
    try:
        i.save()
    except Exception as e:
        print "yichang!!!"
        record_except()
        record_log(i.code)
        record_log(i.date)


    
def ArticleComputer_4_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "start",start_time
    #查询ScrapyD表中数据60天为0的数据,先计算2016年至今的数据
    k = Scrapy_D.objects.filter(price_delta_90_date = 0,date__gt = date_time)
    map(computer_90,k)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
    
    
def  computer_180(i):
    #print "i am here"
    i.price_delta_180_date = comupter_delta(need_price_data,i.code,i.date,180)#更新180天后的价格
    i.charge_delta_180_date = duz(comupter_delta(need_price_data,i.code,i.date,180),i.price_publish_date)#更新180天后的涨跌幅
    i.hightest_price_delta_180_date  = duz(max_price(need_price_data,i.code,i.date,180),i.price_publish_date)#更新180天后的最高涨幅
    try:
        i.save()
    except Exception as e:
        print "yichang!!!"
        record_except()
        record_log(i.code)
        record_log(i.date)


    
def ArticleComputer_5_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "start",start_time
    #查询ScrapyD表中数据60天为0的数据,先计算2016年至今的数据
    k = Scrapy_D.objects.filter(price_delta_180_date = 0,date__gt = date_time)
    map(computer_180,k)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
    
    
    
    
    
    
    
    
    
def computer_publish_price(i):
    i.price_publish_date = comupter_delta(need_price_data,i.code,i.date,0)#更新发布时的价格
    i.save()
def ArticleComputer_1_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "start",start_time

    map(computer_publish_price,Scrapy_D.objects.filter(price_publish_date = 0,date__gt = date_time))

    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
    
    
    
    
def CSH_price_view(request):
    #http://localhost:8080/CSH_price
    #初始化所有股票的价格数据
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "strat!",start_time
    engine = create_engine(db_path)
    #清空原有数据
    CSH_price.objects.all().delete()
    for i in Stock_base.objects.all():
    #    df = ts.get_hist_data(i.code)

        #print i.code
        df = ts.get_k_data(code=i.code)#获取前复权数据

        df.to_sql('myapp_csh_price',engine,if_exists='append')
    result_message = "添加成功！"
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
def stock_detail_today_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    engine = create_engine(db_path)
    today_date = datetime.datetime.now()#今天日期
    today_date = datetime.datetime.now()-timedelta(days = 1)#今天日期，用户测试，往前推一天
    #try:
    #遍历股票档案，获取每只股票当天的交易数据，追加到今天临时表里面
    df = ts.get_today_all()
    #先删除stock_detail_today中的临时数据
    Stock_detail_today.objects.all().delete()
    #df.to_sql('stock_detail',engine)
    df.to_sql('myapp_stock_detail_today',engine,if_exists='append')
    
    #从CSH_price中查询到昨天的收盘价，用于计算今天的收盘价
    CSH_price.objects.filter(date = today_str).delete()#先删除今天的所有股票数据
    date_now = CSH_price.objects.latest("date")#获取昨天的日期
    close_list = CSH_price.objects.filter(date = date_now).values("code","close")#获取昨天的股票数据列表，用于获取昨天的收盘价格
    
    #再将今天临时表中的数据插入到历史表中
    for i in Stock_detail_today.objects.all():
        Stock_detail_history(
                                        date=today_date,
                                        index =i.index,
                                        code = i.code,
                                        name = i.name,
                                        changepercent = i.changepercent,
                                        trade = i.trade,
                                        open = i.open,
                                        high = i.high,
                                        low = i.low,
                                        #close = i.close,这个接口没有当天的收盘价
                                        settlement = i.settlement,
                                        volume = i.volume,
                                        turnoverratio = i.turnoverratio,
                                        amount = i.amount,
                                        per = i.per,
                                        pb = i.pb,
                                        mktcap = i.mktcap,
                                        nmc = i.nmc
                                    ).save()
        #需要计算收盘价
        #t = m["close"]*(1+i.changepercent/100) if m["close"] else i.open
        for m in close_list:
            if m["code"]== i.code:
                #CSH_price增加
                CSH_price(
                                index =i.index,
                                date = today_date.strftime("%Y-%m-%d"),
                                open = i.open,
                                high = i.high,
                                low = i.low,
                                close = (m["close"]*(1+i.changepercent/100) if m["close"] else i.open),#这个接口没有收盘价，需要用开盘价和涨跌幅来计算,这个价格;如果遇到没有价格的情况就用开牌价格；每周刷新一次所有历史数据
                                volume = i.volume,
                                code = i.code,
                         ).save()
                #找到就跳出这次for循环
                break
    result_message = "添加成功！"
    #except:
    #    #没有获取到今日的数据
    #    result_message = "今天不是交易日!"
    #    return HttpResponse(result_message)
        
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)

    
    
def out_put_bill_view(request):
    '''导出所有分析师的能力清单'''
    all_bill = Analyst_power_today.objects.all()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    
    filename = u"Analyst_power-"+time.strftime('%Y-%m-%d-%H-%M-%S')+".xls"
    temp_str = 'attachment; filename='+filename
    response['Content-Disposition'] = temp_str
    workbook = xlwt.Workbook(encoding='utf-8') #创建工作簿
    sheet = workbook.add_sheet("Analyst_power") #创建工作页
    

    row = 1  #行号
    col = 0  #列号
    #表头
    row0 = [
        u'id',
        u'姓名',
        u'公司',
        u'30天涨跌',
        u'30天最高涨跌',
        u'60天涨跌',
        u'60天最高涨跌',
        u'90天涨跌',
        u'90天最高涨跌',
        u'180天涨跌',
        u'180天最高涨跌',
        ]
    for i in range(0,len(row0)):
        sheet.write(0,i,row0[i])

    
    for i in all_bill:
        sheet.write(row,col,i.id)
        sheet.write(row,col+1,i.name)
        sheet.write(row,col+2,i.company)
        sheet.write(row,col+3,i.power_30)
        sheet.write(row,col+4,i.power_30_high)
        sheet.write(row,col+5,i.power_60)
        sheet.write(row,col+6,i.power_60_high)
        sheet.write(row,col+7,i.power_90)
        sheet.write(row,col+8,i.power_90_high)
        sheet.write(row,col+9,i.power_180)
        sheet.write(row,col+10,i.power_180_high)
        row = row+1
    workbook.save(response) 
    
    return response

    
def out_put_bill_2_view(request):
    '''导出所有分析师的能力清单'''
    
    all_bill = Scrapy_D.objects.filter(date__gt = date_time)
    #all_bill = Scrapy_D.objects.all()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    
    filename = u"Analyst_power-"+time.strftime('%Y-%m-%d-%H-%M-%S')+".xlsx"
    temp_str = 'attachment; filename='+filename
    response['Content-Disposition'] = temp_str
    workbook = xlwt.Workbook(encoding='utf-8') #创建工作簿
    sheet = workbook.add_sheet("Analyst_power") #创建工作页
    

    row = 1  #行号
    col = 0  #列号
    #表头
    row0 = [
        u'id',
        u'股票代码',
        u'发布日期',
        u'标题',
        u'公司',
        u'分析师姓名',
        u'内容',
        u'是否参与计算',
        u'发布时价格',
        
        u'30天后日期',
        u'30天后价格',
        u'30天后涨幅',
        u'30天后最大涨幅',
        
        u'60天后日期',
        u'60天后价格',
        u'60天后涨幅',
        u'60天后最大涨幅',
        
        u'90天后日期',
        u'90天后价格',
        u'90天后涨幅',
        u'90天后最大涨幅',
        
        u'180天后日期',
        u'180天后价格',
        u'180天后涨幅',
        u'180天后最大涨幅',
        
        ]
    for i in range(0,len(row0)):
        sheet.write(0,i,row0[i])

    
    for i in all_bill:
        sheet.write(row,col,i.id)
        sheet.write(row,col+1,i.code)
        sheet.write(row,col+2,i.date)
        sheet.write(row,col+3,i.title)
        sheet.write(row,col+4,i.company)
        sheet.write(row,col+5,i.name)
        sheet.write(row,col+6,i.content)
        sheet.write(row,col+7,i.boolean_str)
        sheet.write(row,col+8,i.price_publish_date)
        sheet.write(row,col+9,i.delta_30_date)
        sheet.write(row,col+10,i.price_delta_30_date)
        sheet.write(row,col+11,i.charge_delta_30_date)
        sheet.write(row,col+12,i.hightest_price_delta_30_date)
        sheet.write(row,col+13,i.delta_60_date)
        sheet.write(row,col+14,i.price_delta_60_date)
        sheet.write(row,col+15,i.charge_delta_60_date)
        sheet.write(row,col+16,i.hightest_price_delta_60_date)
        sheet.write(row,col+17,i.delta_90_date)
        sheet.write(row,col+18,i.price_delta_90_date)
        sheet.write(row,col+19,i.charge_delta_90_date)
        sheet.write(row,col+20,i.hightest_price_delta_90_date)
        sheet.write(row,col+21,i.delta_180_date)
        sheet.write(row,col+22,i.price_delta_180_date)
        sheet.write(row,col+23,i.charge_delta_180_date)
        sheet.write(row,col+24,i.hightest_price_delta_180_date)
        row = row+1
    workbook.save(response) 
    
    return response
    
def out_put_bill_3_view(request):
    '''导出所有分析师的能力清单'''
    #csv格式，suoyouScrapy_D的数据，10W多条
    
    #all_bill = Scrapy_D.objects.filter(date__gt = date_time)
    all_bill = Scrapy_D.objects.all()

    response = HttpResponse(content_type='text/csv')
    
    filename = u"Analyst_power-"+time.strftime('%Y-%m-%d-%H-%M-%S')+".csv"
    temp_str = 'attachment; filename='+filename
    response['Content-Disposition'] = temp_str

    writer = csv.writer(response)
    

    #表头
    row0 = [
        u'id',
        u'股票代码',
        u'发布日期',
        u'标题',
        u'公司',
        u'分析师姓名',
        u'内容',
        u'是否参与计算',
        u'发布时价格',
        
        u'30天后日期',
        u'30天后价格',
        u'30天后涨幅',
        u'30天后最大涨幅',
        
        u'60天后日期',
        u'60天后价格',
        u'60天后涨幅',
        u'60天后最大涨幅',
        
        u'90天后日期',
        u'90天后价格',
        u'90天后涨幅',
        u'90天后最大涨幅',
        
        u'180天后日期',
        u'180天后价格',
        u'180天后涨幅',
        u'180天后最大涨幅',
        
        ]
    writer.writerow(row0)

    for i in all_bill:
        t=[]
        t.append(i.id)
        t.append(i.id)
        t.append(i.code)
        t.append(i.date)
        t.append(i.title)
        t.append(i.company)
        t.append(i.name)
        t.append(i.content)
        t.append(i.boolean_str)
        t.append(i.price_publish_date)
        t.append(i.delta_30_date)
        t.append(i.price_delta_30_date)
        t.append(i.charge_delta_30_date)
        t.append(i.hightest_price_delta_30_date)
        t.append(i.delta_60_date)
        t.append(i.price_delta_60_date)
        t.append(i.charge_delta_60_date)
        t.append(i.hightest_price_delta_60_date)
        t.append(i.delta_90_date)
        t.append(i.price_delta_90_date)
        t.append(i.charge_delta_90_date)
        t.append(i.hightest_price_delta_90_date)
        t.append(i.delta_180_date)
        t.append(i.price_delta_180_date)
        t.append(i.charge_delta_180_date)
        t.append(i.hightest_price_delta_180_date)
        writer.writerow(row0)

    return response
    
def record_except():
    #记录异常内容
    f=open("e:/test/myweb/log_yichang","a+")
    traceback.print_exc(file=f)   
    f.flush()   
    f.close()
def record_log(t):
    '''记录哪个股票出现了异常'''
    log_f = file("e:/test/myweb/log_content","a+") #日志文件
    log_f.write(t+"\n")
    log_f.close()

date_now = datetime.datetime.now()
def  except_new(i):
    #如果发布研报时间比上市时间晚60天以上，则参与计算
    for m in stock_base_data:
        if m["code"] == i.code :
            i.boolean_str=0
            try:
                date_time_gap = date_now-datetime.datetime.strptime(str(m["timeToMarket"]),'%Y%m%d')
                if date_time_gap.days>60:
                    i.boolean_str=1
            except:
                i.boolean_str=0
            break
    try:
        i.save()
    except Exception as e:
        print "yichang!!!"
        record_except()
        record_log(i.code)
        record_log(i.date)


    
def ArticleComputer_6_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print "start",start_time
    #查询ScrapyD表中数据发布研报时间比上市时间晚60天，否则不参与计算
    k = Scrapy_D.objects.filter(date__gt = date_time)
    map(except_new,k)
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    