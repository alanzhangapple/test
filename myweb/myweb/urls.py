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
    #3.计算每条研报数据的价格，发布时价格、30天后价格、60天后价格、90天后价格
    url(r'^ArticleComputer$', 'myapp.views.ArticleComputer_view', name='ArticleComputer_view'),    
    #4.计算截止到今天的分析师的能力评估
    url(r'^Analyst_power_today$', 'myapp.views.Analyst_power_today_view', name='Analyst_power_today_view'),
    #5.每天将分析师的能力数据做备份
    url(r'^Analyst_power_history$', 'myapp.views.Analyst_power_history_view', name='Analyst_power_history_view'),
    
    url(r'^CSH_price$', 'myapp.views.CSH_price_view', name='CSH_price_view'),#第一次初始化所有的股票数据
]
