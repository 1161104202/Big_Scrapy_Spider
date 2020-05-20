# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.get_md5_hex import get_md5
from BigB2BSpider.items import BaFangZiYuanWangspiderItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class BaFangZiYuanWangSpider(CrawlSpider):
    name = "b2b168"
    allowed_domains = ['b2b168.com','www.b2b168.com']
    start_urls = ['https://www.b2b168.com/page-company.html']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566177749; CCKF_visitor_id_92126=1219631166; yunsuo_session_verify=db1a03528b7dfe197918cf533946c447; bdshare_firstime=1566178685689; Hm_lpvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566178686",
            # "Host": "jamesni139.tybaba.com",
            # "Referer": "http://jamesni139.tybaba.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        },
        # 不验证SSL证书
        "DOWNLOAD_HANDLERS_BASE": {
            'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
            'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        },
        # "DOWNLOAD_HANDLERS": {
        #     'http': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'},
    }

    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='map']//ul[contains(@class,'c-hangye')]//li//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='mach_list clearfix']//dd//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='list-right']//ul[@class='list']//li//div[1]//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='pages']//a[contains(text(),'下页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//a[contains(text(),'联系方式')]")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        pattern = re.compile(r'<meta name="description" content="(.*?)"/>',re.S)
        pattern1 = re.compile(r'<span>主营：</span>(.*?)</p>',re.S)
        pattern2 = re.compile(r'<div class="com-name">(.*?)</div>',re.S)
        pattern3 = re.compile(r'联 系 人： <a class=b2>(.*?)</a>',re.S)
        pattern4 = re.compile(r'电　　话： (.*?)<br />',re.S)
        pattern5 = re.compile(r'传　　真： (.*?)<br />', re.S)
        pattern6 = re.compile(r'移动电话： (.*?)<br />', re.S)
        pattern7 = re.compile(r'地　　址： (.*?)<br />', re.S)
        pattern8 = re.compile(r'主要经营(.*?)<br />', re.S)

        pattern9 = re.compile(r'<ul class="company">(.*?)</ul>', re.S)
        pattern10 = re.compile(r'主要经营(.*?)<br />', re.S)
        pattern11 = re.compile(r'ShowMap\("divMap","(.*?)","(.*?)", "(.*?)"\);', re.S)
        pattern12 = re.compile(r'>地址：(.*?) <a', re.S)
        pattern13 = re.compile(r'<dt>固定电话：</dt><dd>(.*?)</dd>', re.S)
        pattern14 = re.compile(r'<dt>联系人：</dt><dd>(.*?)</dd>', re.S)
        pattern15 = re.compile(r'<dt>移动电话：</dt><dd>(.*?)</dd>', re.S)
        pattern16 = re.compile(r'<dt>传真号码：</dt><dd>(.*?)</dd>', re.S)

        if response.status == 200:
            try:
                item = BaFangZiYuanWangspiderItem()
                item["company_Name"] = re.findall(pattern11,response.text)[0][0] if re.findall(pattern11,response.text) else ''
                item["company_address"] = re.findall(pattern11,response.text)[0][1] if re.findall(pattern11,response.text) else ''
                item["linkman"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
                item["telephone"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
                item["phone"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
                item["contact_Fax"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
                item["contact_QQ"] = ''
                item["E_Mail"] = ''
                item["kind"] = ",".join(re.findall(pattern1,response.text) if re.findall(pattern1,response.text) else '')
                item["Source"] = response.url
                item["province"] = re.findall(pattern11,response.text)[0][2].split(' ')[0] if re.findall(pattern11,response.text) else ''
                item["city_name"] = re.findall(pattern11,response.text)[0][2].split(' ')[1] if re.findall(pattern11,response.text) else ''

                if item["company_Name"]:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
                item["company_id"] = get_md5(item["company_Name"])

                if item["kind"]:
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                        .replace(',', '|').replace('，', '|').replace('.', '').strip()
                else:
                    try:
                        item["kind"] = "".join(re.findall(pattern10,response.text)) if re.findall(pattern10,response.text) else ''
                    except:
                        item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
                else:
                    try:
                        item["linkman"] = "".join(re.findall(pattern14,response.text)) if re.findall(pattern14,response.text) else ''
                    except:
                        item["linkman"] = ''
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if item["phone"]:
                    item["phone"] = self.cw.search_phone_num(item["phone"])
                else:
                    try:
                        item["phone"] = "".join(re.findall(pattern15,response.text)) if re.findall(pattern15,response.text) else ''
                    except:
                        item["phone"] = ''

                item["phone"] = self.cw.search_phone_num(item["phone"])

                if item["telephone"]:
                    item["telephone"] = self.cw.search_telephone_num(item["telephone"])
                else:
                    try:
                        item["telephone"] = "".join(re.findall(pattern13, response.text)) if re.findall(pattern13, response.text) else ''
                    except:
                        item["telephone"] = ''

                item["telephone"] = self.cw.search_telephone_num(item["telephone"])

                if item["contact_Fax"]:
                    item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
                else:
                    try:
                        item["contact_Fax"] = "".join(re.findall(pattern16, response.text)) if re.findall(pattern16, response.text) else ''
                    except:
                        item["contact_Fax"] = ''

                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

                if item["E_Mail"]:
                    item["E_Mail"] = self.cw.search_email(item["E_Mail"])
                else:
                    item["E_Mail"] = ''

                if item["E_Mail"]:
                    try:
                        item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
                    except:
                        item["contact_QQ"] = ''
                else:
                    item["contact_QQ"] = ''

                if item["company_address"]:
                    item["company_address"] = self.cw.search_address(item["company_address"])
                else:
                    item["company_address"] = ''

                yield item
            except:
                return


if __name__ == '__main__':
    execute(["scrapy", "crawl", "b2b168"])