# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from BigB2BSpider.items import JianShuWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute


class JianShuWangSpider(CrawlSpider):
    name = "jianshu"
    allowed_domains = ['www.jianshu.com']
    start_urls = ['https://www.jianshu.com/']
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        # 'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Host": "www.kusoba.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }

    def parse(self, response):
        item = JianShuWangItem()
        li_list = response.xpath("//div[@id='list-container']/ul//li")
        for li in li_list:
            item["title"] = li.xpath(".//a[@class='title']/text()").getall()
            item["diamond"] = "".join(li.xpath(".//i[@class='iconfont ic-paid1']/..//text()").getall())
            item["author"] = li.xpath(".//a[@class='nickname']/text()").get()
            item["comments"] = "".join(li.xpath(".//i[@class='iconfont ic-list-comments']/..//text()").getall())
            item["like"] = "".join(li.xpath(".//i[@class='iconfont ic-list-like']/..//text()").getall())
            item["money"] = "".join(li.xpath(".//i[@class='iconfont ic-list-money']/..//text()").getall())

            if item["diamond"]:
                item["diamond"] = self.replace_str(item["diamond"])
            if item["author"]:
                item["author"] = self.replace_str(item["author"])
            if item["comments"]:
                item["comments"] = self.replace_str(item["comments"])
            if item["like"]:
                item["like"] = self.replace_str(item["like"])
            if item["money"]:
                item["money"] = self.replace_str(item["money"])

            yield item

    def replace_str(self,text):
        if text:
            text = text.replace(' ', '').strip()
            return text
        else:
            return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "jianshu"])