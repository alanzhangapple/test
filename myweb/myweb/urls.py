# -*- coding: utf-8 -*-
"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #1.更新每天的股票档案数据
    url(r'^StockBase$', 'myapp.views.stock_base_view', name='stock_base_view'),
    #2.每天等收盘之后，更新股票的价格信息
    url(r'^stock_detail_today$', 'myapp.views.stock_detail_today_view', name='stock_detail_today_view'),
    #3.将今天爬取到的数据转移到Scrapy_D中
    url(r'^ArticleComputer$', 'myapp.views.ArticleComputer_view', name='ArticleComputer_view'),    
    #4.计算截止到今天的分析师的能力评估
    #4.1计算发布时间的价格
    url(r'^ArticleComputer_1$', 'myapp.views.ArticleComputer_1_view', name='ArticleComputer_1_view'),
   
   #4.2计算30天后的数据：价格、涨跌幅、最高涨跌幅
    url(r'^ArticleComputer_2$', 'myapp.views.ArticleComputer_2_view', name='ArticleComputer_2_view'),
    
    #4.3计算60天后的数据：价格、涨跌幅、最高涨跌幅
    url(r'^ArticleComputer_3$', 'myapp.views.ArticleComputer_3_view', name='ArticleComputer_3_view'),
    
    #4.4计算90天后的数据：价格、涨跌幅、最高涨跌幅
    url(r'^ArticleComputer_4$', 'myapp.views.ArticleComputer_4_view', name='ArticleComputer_4_view'),
    
    
    #4.5计算180天后的数据：价格、涨跌幅、最高涨跌幅
    url(r'^ArticleComputer_5$', 'myapp.views.ArticleComputer_5_view', name='ArticleComputer_5_view'),
    
    #4.6计算是否为新股：发布时间必须比上市时间晚60天
    url(r'^ArticleComputer_6$', 'myapp.views.ArticleComputer_6_view', name='ArticleComputer_6_view'),
    
    
    #5.每天计算最新的分析师能力结果
    url(r'^Analyst_power_today$', 'myapp.views.Analyst_power_today_view', name='Analyst_power_today_view'),
    
    #6.每天将分析师的能力数据做备份
    url(r'^Analyst_power_history$', 'myapp.views.Analyst_power_history_view', name='Analyst_power_history_view'),
    
    
    
    
    
    
    url(r'^CSH_price$', 'myapp.views.CSH_price_view', name='CSH_price_view'),#第一次初始化所有的股票数据
    url(r'^out_put_bill$', 'myapp.views.out_put_bill_view', name='out_put_bill_view'),#导出股票分析师的能力结果数据
    url(r'^out_put_bill_2$', 'myapp.views.out_put_bill_2_view', name='out_put_bill_2_view'),#导出股票分析师的能力结果数据
]
