# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from scrapy.item import Field
from myapp.models import Person
from myapp.models import Person
from myapp.models import Scrapy_B,Scrapy_C,Scrapy_D
from myapp.models import Analyst

class PersonItem(DjangoItem):
    # fields for this item are automatically created from the django model
    django_model = Person



class PersonItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = Person

class Scrapy_B_Item(DjangoItem):
    django_model =  Scrapy_B
    
class AnalystItem(DjangoItem):
    django_model = Analyst