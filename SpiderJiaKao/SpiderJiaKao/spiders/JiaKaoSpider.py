# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
import re
from SpiderJiaKao.items import JiaKaoItem
import time
from scrapy.http import Request


class JiakaospiderSpider(scrapy.Spider):
    name = 'JiaKaoSpider'
    allowed_domains = ['www.ybjk.com']
    start_urls = ['https://www.ybjk.com/tiku/kmy-1501.htm',
                  # 'https://www.ybjk.com/tiku/kmy-1502.htm',
                  # 'https://www.ybjk.com/tiku/kmy-1503.htm',
                  # 'https://www.ybjk.com/tiku/kmy-1504.htm'
                  ]#科一
    # start_urls = ['http://www.ybjk.com/tiku/kms-1511.htm',
    #               'http://www.ybjk.com/tiku/kms-1512.htm',
    #               'http://www.ybjk.com/tiku/kms-1513.htm',
    #               'http://www.ybjk.com/tiku/kms-1514.htm',
    #               'http://www.ybjk.com/tiku/kms-1515.htm',
    #               'http://www.ybjk.com/tiku/kms-1516.htm',
    #               'http://www.ybjk.com/tiku/kms-1517.htm',
    #
    #               ]#科四

    def parse(self, response):

        print("------------开始爬数据-----------------")
        li_list = response.css('.mainBox.tikuBox .list .fcc').extract() #所有题和标签
        for li in li_list:  # li 一道题
            print("======这是一道题=========")
            ti = re.match('.*</b>(.*?)</li>', li).group(1)  # 把没用的标签剔除
            no_img = re.match('.*<a href=.* target="_blank">(.*?)</u>', ti).group(1)  # 取题目里不包含图片的部分
            try:
                img_url = re.match('.*<img src="(.*?)">.*', ti).group(1)  # 取题目里的图片url
            except:
                img_url = ""

            answer = re.match('.*<br>答案：(.*?)<u>查看分析', no_img).group(1)  # 取答案并把对错改为AB
            if '对' in answer:
                answer = 'A'
            if '错' in answer:
                answer = 'B'

            question_option = re.match('(.*?)<br><br>.*', no_img).group(1)  # 问题和选项
            try:
                question = re.match('(.*?)<br>.*', question_option).group(1).strip()  # 问题
                option_a = re.match('.*<br>A、(.*?)<br>B.*', question_option).group(1)  # 选项A
                option_b = re.match('.*<br>B、(.*?)<br>C.*', question_option).group(1)  # 选项A
                option_c = re.match('.*<br>C、(.*?)<br>D.*', question_option).group(1)  # 选项A
                option_d = re.match('.*<br>D、(.*?)<br>.*', no_img).group(1)
            except:
                question = question_option
                option_a = '对'
                option_b = '错'
                option_c = ''
                option_d = ''
            if option_c.__len__()==0:
                type = "判断"
            if option_c.__len__()>0:
                type = "单选"
            if answer.__len__()>1:
                type = "多选"
            taotiid = 8
            createtime =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            # print(createtime)
            # print(question)
            # print(type)
            # print(option_a)
            # print(option_b)
            # print(option_c)
            # print(option_d)
            # print(img_url)
            # print(answer)
            #
            # jiaItem = JiaKaoItem()
            # jiaItem['optiona'] = option_a
            # jiaItem['optionb'] = option_b
            # jiaItem['optionc'] = option_c
            # jiaItem['optiond'] = option_d
            # jiaItem['subject'] = question
            # jiaItem['taotiid'] = taotiid
            # jiaItem['createtime'] = createtime
            #
            # jiaItem['image_url'] = img_url
            # jiaItem['answer'] = answer
            # jiaItem['type'] = type
            # yield jiaItem

        # nextUrl_list = response.css(".mainBox.tikuBox .list .PageL a").extract()
        # nextUrl_list = ",".join(nextUrl_list)
        # print(nextUrl_list)
        # try:
        #     nextUrl = re.match('.*<a href="(.*?)">下页</a>', nextUrl_list).group(1)
        # except:
        #     nextUrl = ''
        # print(nextUrl)
        # if nextUrl:
        #     yield Request(url=parse.urljoin(response.url, nextUrl), callback=self.parse)
        pass


