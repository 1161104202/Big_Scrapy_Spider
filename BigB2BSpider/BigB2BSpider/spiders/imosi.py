# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import MouSiWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class MouSiWangSpider(CrawlSpider):
    name = "imosi"
    allowed_domains = ['www.imosi.com','company.imosi.com']
    start_urls = ['http://company.imosi.com/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
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
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='box']//table//span//a")),callback='parse_items',follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='pagination']//a[contains(text(),'下页')]")),follow=True),

    )

    def parse_items(self, response):
        div_list = response.xpath("//div[@id='div1']//div[@class='gy_list_libox']")
        for div in div_list:
            item = MouSiWangItem()
            item["company_Name"] = div.xpath(".//span[contains(text(),'商家名称：')]/a/text()").extract_first()
            item["kind"] = div.xpath(".//span[contains(text(),'主营业务：')]/following-sibling::span/text()").extract_first()
            item["company_address"] = div.xpath(".//span[contains(text(),'商家地址：')]/@title").extract_first()
            item["linkman"] = div.xpath(".//span[contains(text(),'联系人：')]/text()").extract_first()
            item["telephone"] = div.xpath(".//span[contains(text(),'联系电话：')]/text()").extract_first()
            item["phone"] = div.xpath(".//span[contains(text(),'手机：')]/text()").extract_first()
            item["contact_Fax"] = div.xpath(".//span[contains(text(),'联系电话：')]/a/text()").extract_first()
            item["contact_QQ"] = div.xpath(".//img[@class='gy_list_message_dn']/../@href").extract_first()
            item["E_Mail"] = div.xpath(".//span[contains(text(),'电子邮箱：')]/a/text()").extract_first()
            item["Source"] = response.url
            item["province"] = ""
            item["city_name"] = ""

            if item["company_Name"]:
                if "（" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('（')[0]
                elif "(" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('(')[0]
                else:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(' ', '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|').replace('、', '|')\
                    .replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
            else:
                item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"]
            else:
                item["linkman"] = ''
            item["linkman"] = self.cw.search_linkman(item["linkman"])

            if item["telephone"]:
                item["telephone"] = item["telephone"]
            else:
              item["telephone"] = ''
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])

            if item["phone"]:
                item["phone"] = item["phone"]
            else:
                try:
                    item["phone"] = self.cw.search_phone_num(item["telephone"])
                except:
                    item["phone"] = ''
            item["phone"] = self.cw.search_phone_num(item["phone"])



            if item["contact_Fax"]:
                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
            else:
                item["contact_Fax"] = ''

            if item["E_Mail"]:
                item["E_Mail"] = self.cw.search_email(item["E_Mail"])
            else:
                item["E_Mail"] = ''

            if item["contact_QQ"]:
                item["contact_QQ"] = item["contact_QQ"].replace("Q Q：",'')
            else:
                try:
                    item["contact_QQ"] = "".join(re.findall(r'(\d+)@qq.com',item["E_Mail"])) \
                        if re.findall(r'(\d+)@qq.com',item["E_Mail"]) else ''
                except:
                    item["contact_QQ"] = ''
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

            if item["company_address"]:
                item["company_address"] = self.cw.search_address(item["company_address"])
            else:
                item["company_address"] = ''

            yield item


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "imosi"])