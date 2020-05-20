# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import WuYouJiaoYiWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class WuYouJiaoYiWangSpider(CrawlSpider):
    name = "ec51"
    allowed_domains = ['www.ec51.com','ec51.com']
    start_urls = ['https://www.ec51.com/site/company.html']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            # "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566177749; CCKF_visitor_id_92126=1219631166; yunsuo_session_verify=db1a03528b7dfe197918cf533946c447; bdshare_firstime=1566178685689; Hm_lpvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566178686",
            # "Host": "jamesni139.tybaba.com",
            # "Referer": "http://jamesni139.tybaba.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 420,
        },
        # 不验证SSL证书
        # "DOWNLOAD_HANDLERS_BASE": {
        #     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
        #     'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
        #     'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
        #     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        # },
        # "DOWNLOAD_HANDLERS": {
        #     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'},
    }

    def parse(self, response):
        div_list = response.xpath("//div[@class='flex-item product-wrap']//div[@class='product flex']")
        for div in div_list:
            item = WuYouJiaoYiWangItem()
            item["company_Name"] = div.xpath(".//a[@class='title ea']/text()").get()
            item["kind"] = div.xpath(".//p[contains(text(),'经营范围：')]/text()").get()
            item["company_address"] = div.xpath(".//p[contains(text(),'公司地址：')]/text()").get()
            item["linkman"] = ''
            item["telephone"] = div.xpath(".//p[contains(text(),'联系方式：')]/text()").get()
            item["phone"] = div.xpath(".//p[contains(text(),'联系方式：')]/text()").get()
            item["contact_Fax"] = ''
            item["contact_QQ"] = ''
            item["E_Mail"] = ''
            item["Source"] = response.url
            item["province"] = ""
            item["city_name"] = ""

            if item["company_Name"]:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(' ', '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品|经营范围：', '', item["kind"]).replace('-', '|')\
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
            else:
                try:
                    item["kind"] = ",".join(response.xpath("//p[contains(text(),'公司标签：')]//a/text()").getall())
                    item["kind"] = item["kind"].replace(' ', '|')
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品|经营范围：', '', item["kind"]).replace('-', '|') \
                        .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.',
                                                                                                         '').strip()
                except:
                    item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"]
            else:
                item["linkman"] = ''
            item["linkman"] = self.cw.search_linkman(item["linkman"])

            if item["phone"]:
                item["phone"] = self.cw.search_phone_num(item["phone"])
            else:
                item["phone"] = ''

            if item["telephone"]:
                item["telephone"] = self.cw.search_telephone_num(item["telephone"])
            else:
              item["telephone"] = ''

            if item["contact_Fax"]:
                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
            else:
                item["contact_Fax"] = ''

            if item["E_Mail"]:
                item["E_Mail"] = self.cw.search_email(item["E_Mail"])
            else:
                item["E_Mail"] = ''

            if item["contact_QQ"]:
                item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
            else:
                try:
                    item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
                except:
                    item["contact_QQ"] = ''

            if item["company_address"]:
                item["company_address"] = self.cw.search_address(item["company_address"])
            else:
                item["company_address"] = ''

            yield item

        next_page_url = response.xpath("//li[@class='next']//a[contains(text(),'下一页')]/@href").get()
        if next_page_url:
            next_page_url = "https://www.ec51.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "ec51"])