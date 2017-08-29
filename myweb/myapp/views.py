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
def stock_base_view(request):
    
    #获取数据库操作引擎
    #1. 更新股票档案数据库
    #2. 更细股票每天的涨跌幅数据
    engine = create_engine(r'sqlite:///E:\test\myweb\db\myweb.db')
    df = ts.get_stock_basics()
    
    #先清空数据，然后再添加
    print Stock_base.objects.all().count()
    Stock_base.objects.all().delete()
    df.to_sql('myapp_stock_base',engine,if_exists='append')
    result_message = "添加成功！"
    return HttpResponse(result_message)
    


def Analyst_power_today_view(request):
    #localhost:8080/Analyst_power_today
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    Analyst_power_today.objects.all().delete()#先删除掉所有记录
    #统计每个分析师在每个周期的平均涨跌幅，30天，60天，90天，180天
    for k in Analyst.objects.all():
        t = Scrapy_D.objects.filter(name = k.name)

        if t:
            Analyst_power_today(
                                name = t[0].name,
                                company = t[0].company,
                                
                                power_30 = t.aggregate(Avg('charge_delta_30_date'))["charge_delta_30_date__avg"],
                                power_60 = t.aggregate(Avg('charge_delta_60_date'))["charge_delta_60_date__avg"],
                                power_90 = t.aggregate(Avg('charge_delta_90_date'))["charge_delta_90_date__avg"],
                                power_180 = t.aggregate(Avg('charge_delta_180_date'))["charge_delta_180_date__avg"],
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
        return a/b-1
    
def comupter_delta(need_price_data,code,publish_date,delta):
    #计算间隔时间的股票价格，如30天之后的价格
    #input：股票编码合并数据，股票编码，发布时间，延迟时间
    #output:价格，此处价格为收盘价

    
    last_date = publish_date + timedelta(days = delta)
    date_publish_weekday = last_date.weekday()
    #如果遇到周六周日，统一记作周五
    if date_publish_weekday == 6:
        last_date = last_date-datetime.timedelta(days = 2 )

    if date_publish_weekday == 5:
        last_date = last_date-datetime.timedelta(days = 1 )
    

    for i in need_price_data:
        if i["code"]== code and i["date"]==last_date.strftime("%Y-%m-%d"):
            price_data = i["close"]
        else:
            #如果查不到股票价格，价格就是0
            price_data = 0
    return price_data
    
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
    print "需要删除数据条数：",t.count()
    t.delete()

    for k in Scrapy_B.objects.all():
        print k.code,k.name
        #price_publish = comupter_delta(k.code,k.date,0)#发布日期价格
        Scrapy_D(
                    code = k.code,
                    date = k.date,
                    title = k.title,
                    company = k.company,
                    name = k.name,
                    
                    price_publish_date = 0,#从发布日期往后推0天的价格
                    
                    delta_30_date = k.date + timedelta(days = 30),
                    price_delta_30_date = 0,#从发布日期往后推30天
                    charge_delta_30_date = 0, #30天后涨跌幅
                    
                    delta_60_date = k.date + timedelta(days = 60),
                    price_delta_60_date = 0,#从发布日期往后推60天
                    charge_delta_60_date = 0,#60天后涨跌幅
                    
                    delta_90_date = k.date + timedelta(days = 90),
                    price_delta_90_date = 0,#从发布日期往后推90天
                    charge_delta_90_date = 0,
                    #90天后涨跌幅
                    
                    delta_180_date = k.date + timedelta(days = 180),
                    price_delta_180_date = 0,#从发布日期往后推180天
                    charge_delta_180_date =0,#180天后涨跌幅
                ).save()
                
    #更新Sccrapy_D表中，发布日期、30天后、60天后、90天后、180天后为空的数据
    
    #从CHS_price中查询一次所有的数据
    
    Scrapy_B_code_list = Scrapy_B.objects.all().values_list("code",flat=True)
    #print "time 1:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    need_price_data  = CSH_price.objects.filter(code__in = Scrapy_B_code_list).values("code","date","close")

    

    for i in Scrapy_D.objects.filter(price_publish_date = 0):
        i.price_publish_date = comupter_delta(need_price_data,i.code,i.date,0)#更新30天后的价格
        i.save()


    for i in Scrapy_D.objects.filter(price_delta_30_date = 0):
        i.price_delta_30_date = comupter_delta(need_price_data,i.code,i.date,30)#更新30天后的价格
        i.charge_delta_30_date = duz(comupter_delta(need_price_data,i.code,i.date,30),i.price_publish_date)#更新30天后的涨跌幅
        i.save()

    for i in Scrapy_D.objects.filter(price_delta_60_date = 0):
        i.price_delta_60_date = comupter_delta(need_price_data,i.code,i.date,60)#更新60天后的价格
        i.charge_delta_60_date = duz(comupter_delta(need_price_data,i.code,i.date,60),i.price_publish_date)#更新60天后的涨跌幅
        i.save()
    
    for i in Scrapy_D.objects.filter(price_delta_90_date = 0):
        i.price_delta_90_date = comupter_delta(need_price_data,i.code,i.date,90)#更新90天后的价格
        i.charge_delta_90_date = duz(comupter_delta(need_price_data,i.code,i.date,90),i.price_publish_date)#更新90天后的涨跌幅
        i.save()
        
    for i in Scrapy_D.objects.filter(price_delta_180_date = 0):
        i.price_delta_180_date = comupter_delta(need_price_data,i.code,i.date,180)#更新180天后的价格
        i.charge_delta_180_date = duz(comupter_delta(need_price_data,i.code,i.date,180),i.price_publish_date)#更新180天后的涨跌幅
        i.save()
    
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)

def CSH_price_view(request):
    #http://localhost:8080/CSH_price
    #初始化所有股票的价格数据
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    engine = create_engine(r'sqlite:///E:\test\myweb\db\myweb.db')
    #清空原有数据
    CSH_price.objects.all().delete()
    for i in Stock_base.objects.all():
    #    df = ts.get_hist_data(i.code)
        df = ts.get_k_data(code=i.code)
        df.to_sql('myapp_csh_price',engine,if_exists='append')
    result_message = "添加成功！"
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    result_message = "添加成功！开始时间："+start_time+"结束时间："+end_time
    return HttpResponse(result_message)
    
def stock_detail_today_view(request):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    engine = create_engine(r'sqlite:///E:\test\myweb\db\myweb.db')
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

    
    
    
    
    
    
    
    
    
    