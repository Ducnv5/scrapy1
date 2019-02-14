# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import os
import logging
import re
import json
import random
import sys
from urllib.parse import urlparse
import urllib
import pandas as pd
from bs4 import BeautifulSoup
import time

from datetime import datetime
import time
from Sendo.items import SendoShopItem
#from Sendo.settings import SHEET_ID
import requests

#from scrapy.utils.project import get_project_settings    
#settings = get_project_settings()
from Sendo.settings import URL_CSV
from Sendo.items import SendoShopItem



class SendoShopSpider(scrapy.Spider):
    name = 'SendoShopSpider'
    handle_httpstatus_list = [404]
    logger = logging.getLogger('productcollectpipeline')


    def __init__(self):
        self.df_urls = pd.read_csv(URL_CSV)
    #START SPIDER HERE
    
    def start_requests(self):
        for i, row in self.df_urls.iterrows():
            #self.logger.info("start_requests item_type: " + str(item_type) + " page_no: " + str(page_no))
            #time.sleep(0.5)
            item = SendoShopItem()
            url = row["url"] + "/thong-tin-shop/"
            item["phone_number"] = ""
            item["address"] = ""
            item["email"] = ""
            item["category"] = ""
            item["website"] = ""
            item["shop_name"] = ""
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['item'] = item
            yield request
    def parse(self, response):
        item = response.meta['item']
        #self.logger.info("parse_ram_detail item: " + str(item))
        try:
            shop_name = response.xpath("//span[@class='shop-name shop_color']/text()").extract_first()
            categories = response.xpath("//div[@class='ttl-shop ']/span/text()").extract()
            item["shop_name"] += shop_name
            item["category"] += str(categories)
        except Exception as e:
            self.logger.info("exception when extract shop name, category, detail: " + str(e))
        
        shop_infos = response.xpath("//div[@class='cont-shop-inf']/div").extract()
        property_dict = {"address": "địa chỉ", "phone_number": "điện thoại", "email": "email", "website": "website"}
        for field in property_dict:
            for shop_info in shop_infos:
                if property_dict[field] in shop_info.lower():
                    try:
                        property_value = re.search("<span>(.*)</span>", shop_info).group(1)
                        item[field] += property_value
                        break
                    except Exception as e:
                        self.logger.info("exception when extract {0}, detail: ".format(field) + str(e))
            #self.logger.info("Exception in parse_url: " + str(e))
        return item
