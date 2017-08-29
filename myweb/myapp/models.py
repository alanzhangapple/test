# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=32)

class Analyst(models.Model):
    name = models.CharField(max_length=32)
    company = models.CharField(max_length=32)

class Scrapy_B(models.Model):
    code = models.CharField(max_length=32)  
    #analyst =  models.CharField(max_length=32)
    date = models.DateField(auto_now=False) 
    title = models.CharField(max_length=100)
    
    company = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class Scrapy_C(models.Model):
    code = models.CharField(max_length=32)  
    #analyst =  models.CharField(max_length=32)
    date = models.DateField(auto_now=False) 
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100,verbose_name = "ICG")
    name = models.CharField(max_length=100)

class Scrapy_D(models.Model):
    #记录研报的股票价格、时间、各个区间的价格明细
    code = models.CharField(max_length=32)  
    #analyst =  models.CharField(max_length=32)
    date = models.DateField(auto_now=False) 
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100,default = "ICG")
    name = models.CharField(max_length=100,default = "ICG")
    
    #记录价格信息，如果时间是周末，则记录上个周五的价格
    price_publish_date = models.FloatField(default = 0.0)#发布时候的价格
    
    delta_30_date = models.DateField(default=datetime.datetime.now().date())#30天后的时间
    price_delta_30_date = models.FloatField(default = 0.0)#30天后的股价
    charge_delta_30_date = models.FloatField(default = 0.0)#30天后的涨幅
    
    delta_60_date = models.DateField(default=datetime.datetime.now().date())#60天后的时间
    price_delta_60_date = models.FloatField(default = 0.0)#60天后的股价
    charge_delta_60_date = models.FloatField(default = 0.0)#60天后的涨跌

    delta_90_date = models.DateField(default=datetime.datetime.now().date())#90天后的时间
    price_delta_90_date = models.FloatField(default = 0.0)#90天后的股价
    charge_delta_90_date = models.FloatField(default = 0.0)#90天后的涨跌

    delta_180_date = models.DateField(default=datetime.datetime.now().date())#180天后的时间
    price_delta_180_date = models.FloatField(default = 0.0)#180天后的股价
    charge_delta_180_date = models.FloatField(default = 0.0)#180天后的涨跌
    
class Stock_base(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    industry = models.CharField(max_length=32)
    area = models.CharField(max_length=32)
    pe = models.FloatField()
    outstanding = models.FloatField()
    totals = models.FloatField()
    totalAssets = models.FloatField()
    liquidAssets = models.FloatField()
    fixedAssets = models.FloatField()
    reserved = models.FloatField()
    reservedPerShare = models.FloatField()
    esp = models.FloatField()
    bvps = models.FloatField()
    pb = models.FloatField()
    timeToMarket = models.IntegerField()
    undp = models.FloatField()
    perundp = models.FloatField()
    rev = models.FloatField()
    profit = models.FloatField()
    gpr = models.FloatField()
    npr = models.FloatField()
    holders = models.FloatField()

class Stock_detail_today(models.Model):
    
    #date = models.DateField(auto_now=True)
    index = models.IntegerField()
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    changepercent = models.FloatField()
    trade = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    settlement = models.FloatField()
    volume = models.IntegerField()
    turnoverratio = models.FloatField()
    amount = models.IntegerField()
    per = models.FloatField()
    pb = models.FloatField()
    mktcap = models.FloatField()
    nmc = models.FloatField()
    '''
    date：日期
    open：开盘价
    high：最高价
    close：收盘价
    low：最低价
    volume：成交量
    price_change：价格变动
    p_change：涨跌幅
    ma5：5日均价
    ma10：10日均价
    ma20:20日均价
    v_ma5:5日均量
    v_ma10:10日均量
    v_ma20:20日均量
    turnover:换手率[注：指数无此项]
    '''

class Stock_detail_history(models.Model):
    
    date = models.DateField(default=datetime.datetime.now().date())
    index = models.IntegerField()
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    changepercent = models.FloatField()
    trade = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    settlement = models.FloatField()
    volume = models.IntegerField()
    turnoverratio = models.FloatField()
    amount = models.IntegerField()
    per = models.FloatField()
    pb = models.FloatField()
    mktcap = models.FloatField()
    nmc = models.FloatField()
    
    
class Power_detail(models.Model):
    
    code = models.CharField(max_length=32)  
    #analyst =  models.CharField(max_length=32)
    date = models.DateField(auto_now=False) 
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100,verbose_name = "ICG")
    name = models.CharField(max_length=100)
    
    
    
class CSH_price(models.Model):
    #初始化所有股票的价格数据
    index = models.IntegerField()
    date = models.CharField(max_length=32) 
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()
    code = models.CharField(max_length=32) 

class Analyst_power_today(models.Model):
    #每天最新的分析师涨跌能力
    name = models.CharField(max_length=32) 
    company = models.CharField(max_length=32) 
    
    power_30 = models.FloatField()
    power_60 = models.FloatField()
    power_90 = models.FloatField()
    power_180 = models.FloatField()
    

    
class Analyst_power_history(models.Model):
    #每天最新的分析师涨跌能力
    name = models.CharField(max_length=32) 
    company = models.CharField(max_length=32) 
    
    power_30 = models.FloatField()
    power_60 = models.FloatField()
    power_90 = models.FloatField()
    power_180 = models.FloatField()
    
    date = models.DateField(auto_now=False) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    