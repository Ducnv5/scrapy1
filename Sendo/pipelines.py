# -*- coding: utf-8 -*-
import pandas as pd
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Sendo.settings import URL_CSV, SHOP_INFO_CSV
from Sendo.items import SendoUrlItem, SendoShopItem
import logging

logger = logging.getLogger('productcollectpipeline')

class SendoPipeline(object):
    def __init__(self):
        self.df_urls = pd.DataFrame(columns=['url', 'type'])
        self.df_shop_info = pd.DataFrame(columns=['shop_name', 'phone_number', 'address', 'email', 'category', 'website'])

    def process_item(self, item, spider):
        if isinstance(item, SendoUrlItem):
            self.process_url_item(item, spider)
        elif isinstance(item, SendoShopItem):
            self.process_sendo_shop_item(item, spider)
        else:
            logger.error("No detect any type of item")
            
    def process_url_item(self, item, spider):
        if(item["urls"] != ""):
            urls = [{"url": url,"type": item["type"]} for url in item["urls"].split('"')]
            self.df_urls = self.df_urls.append(urls, ignore_index=True)
            logger.info("process_url_item  result size: " + str(len(self.df_urls)))

    def process_sendo_shop_item(self, item, spider):
        try:
            shop_info = [{'shop_name': item['shop_name'], 'phone_number': item['phone_number'], 'address': item['address'], 'email': item['email'], 'category': item['category'], 'website': item['website'] }]
            self.df_shop_info = self.df_shop_info.append(shop_info, ignore_index=True)
            #logger.info("process_url_item  result size: " + str(len(self.df_urls)))
            logger.info("process_sendo_shop_item  result size: " + str(len(self.df_shop_info)))
            if(len(self.df_shop_info) % 200 == 1):
                self.df_shop_info.to_csv(SHOP_INFO_CSV)
        except Exception as e:
            logger.info(e)
            
    def close_spider(self, spider):
        try:
            if(len(self.df_urls) > 0):
                self.df_urls.to_csv(URL_CSV)
                logger.info("close_spider saved to csv: list of urls")
            if(len(self.df_shop_info) > 0):
                self.df_shop_info.to_csv(SHOP_INFO_CSV)
                logger.info("close_spider saved to csv: list of urls")
        except Exception as e:
            logger.info("fail close_spider : " + str(e))
            
