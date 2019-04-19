# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderjiakaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class JiaKaoItem(scrapy.Item):
    subject = scrapy.Field() #题目
    type = scrapy.Field() #选择类型
    createtime = scrapy.Field() #创建时间
    taotiid = scrapy.Field() #套题id
    optiona = scrapy.Field() #选项A
    optionb = scrapy.Field() #选项B
    optionc = scrapy.Field() #选项C
    optiond = scrapy.Field() #选项D
    answer = scrapy.Field() #答案
    image_url = scrapy.Field() #img路径
