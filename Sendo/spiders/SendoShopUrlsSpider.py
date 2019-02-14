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

from datetime import datetime
import time
from Sendo.items import SendoUrlItem
from Sendo.settings import SENDO_SHOP_NUMBER_OF_PAGE, SENDO_SHOP_LIST_URL

import requests


class SendoShopUrlsSpider(scrapy.Spider):
    name = 'SendoShopUrlsSpider'
    handle_httpstatus_list = [404]

                
    #START SPIDER HERE
    def start_requests(self):
        for page_no in range(1, SENDO_SHOP_NUMBER_OF_PAGE + 1):
            #self.logger.info("start_requests item_type: " + str(item_type) + " page_no: " + str(page_no))
            #time.sleep(0.5)
            item = SendoUrlItem()
            url = SENDO_SHOP_LIST_URL.format(page_no)
            item["type"] = "shop_url"
            item["urls"] = ""
            request = scrapy.Request(url=url, callback=self.parse_url)
            request.meta['item'] = item
            yield request
                        
    def parse_url(self, response):
        item = response.meta['item']
        #self.logger.info("parse_ram_detail item: " + str(item))
        try:
            items_selector = response.xpath("//div[@class='shop-info-boxs']")
            urls = []
            for item_selector in items_selector:
                item_selector_ = scrapy.Selector(text=item_selector.extract())
                url = item_selector_.xpath("//div[@class='shop-name']/a/@href").extract_first()
                if(url):
                    urls.append(url)
            item["urls"] += '"'.join(urls)
            self.logger.info("parse_url item_type: " + str(item["type"]) + " urls: " + str(urls))
        except Exception as e:
            self.logger.info("Exception in parse_url: " + str(e))
        return item
