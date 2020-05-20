# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import QuanQiuHuaMuWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class QuanQiuHuaMuWangSpider(CrawlSpider):
    name = "hmw"
    allowed_domains = ['huamu.cn','www.huamu.cn','ying_love520.huamu.cn']
    start_urls = ['http://www.huamu.cn/Company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
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
        "DOWNLOAD_HANDLERS_BASE": {
            'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
            'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        },
        # "DOWNLOAD_HANDLERS": {
        #     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'},
    }

    rules = (
        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[contains(text(),'联系方式')]/..")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='pageNumber']//a[contains(text(),'下一页')]")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[@class='nav']//a[contains(text(),'联系方式')]")), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        item = QuanQiuHuaMuWangItem()
        if response.text:
            try:
                # 联 系 人： 冯德伟<br>
                pattern = re.compile(r'人：(.*?)<br>',re.S)
                pattern1 = re.compile(r'<span>手机号码：</span> (.*?)<')
                pattern2 = re.compile(r'<span>电话号码：</span> (.*?)<')
                pattern3 = re.compile(r'<span>传真号码：</span> (.*?)<')
                pattern4 = re.compile(r'<span>Email：</span> (.*?)\s*<')
                pattern5 = re.compile(r'>\s*公司地址：(.*?)<',re.S)
                pattern6 = re.compile(r'主营：(.*?)\s*<',re.S)
                pattern7 = re.compile(r'>\s*手机号码：(.*?)  电话号码：(.*?)<',re.S)
                item["company_Name"] = response.xpath("//div[@class='shop-name float-left']/a/@title").get()
                item["kind"] = response.xpath("//div[@class='shop-name float-left']//span/@title").get()
                item["company_address"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
                item["linkman"] = "".join(re.findall(pattern,response.text)[2]) if re.findall(pattern,response.text) else ''
                item["telephone"] = "".join(re.findall(pattern,response.text)[0][1]) if re.findall(pattern,response.text) else ''
                item["phone"] = "".join(re.findall(pattern,response.text)[0][0]) if re.findall(pattern,response.text) else ''
                item["contact_Fax"] = response.xpath("//span[contains(text(),'传真号码')]/..//text()").getall()
                item["contact_QQ"] = response.xpath("//span[contains(text(),'QQ号码')]/..//text()").getall()
                item["E_Mail"] = response.xpath("//span[contains(text(),'邮箱地址')]/..//text()").getall()
                item["Source"] = response.url
                item["province"] = ""
                item["city_name"] = ""

                if item["company_Name"]:
                    item["company_Name"] = re.sub(
                        r'\n|\s|\r|\t|公司名称：|企 业 名 称：', '', item["company_Name"]).replace(' ', '').strip()
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    if "主营产品" in item["kind"]:
                        item["kind"] = item["kind"].split('主营产品：')[-1]
                        item["kind"] = item["kind"].replace(' ', '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"])\
                            .replace('-', '|').replace('、','|').replace(',', '|').replace('，', '|')\
                            .replace(';', '|').replace('.', '').strip()
                    else:
                        item["kind"] = item["kind"]
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品:', '', item["kind"]) \
                            .replace('-', '|').replace('、', '|').replace(',', '|').replace('，', '|') \
                            .replace(';', '|').replace('.', '').strip()
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
                else:
                    item["linkman"] = ''
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if item["phone"]:
                    try:
                        item["phone"] = item["phone"][2]

                    except:
                        item["phone"] = ''
                else:
                    try:
                        item["phone"] = "|".join(re.findall(pattern1,response.text)[0]) if re.findall(pattern1,response.text) else ''
                    except:
                        item["phone"] = ''
                item["phone"] = self.cw.search_phone_num(item["phone"])

                if item["telephone"]:
                    try:
                        item["telephone"] = item["telephone"][2]

                    except:
                        item["telephone"] = ''
                else:
                    try:
                        item["telephone"] = "|".join(re.findall(pattern2,response.text)[0]) if re.findall(pattern2,response.text) else ''
                    except:
                        item["telephone"] = ''
                item["telephone"] = self.cw.search_telephone_num(item["telephone"])

                if item["contact_Fax"]:
                    try:
                        item["contact_Fax"] = item["contact_Fax"][2]

                    except:
                        item["contact_Fax"] = ''
                else:
                    try:
                        item["contact_Fax"] = "|".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
                    except:
                        item["contact_Fax"] = ''

                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

                if item["E_Mail"]:
                    try:
                        item["E_Mail"] = item["E_Mail"][2]

                    except:
                        item["E_Mail"] = ''
                else:
                    try:
                        item["E_Mail"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
                    except:
                        item["E_Mail"] = ''
                item["E_Mail"] = self.cw.search_email(item["E_Mail"])

                if item["contact_QQ"]:
                    try:
                        item["contact_QQ"] = item["contact_QQ"][2]
                        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
                    except:
                        item["contact_QQ"] = ''
                else:
                    try:
                        item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
                    except:
                        item["contact_QQ"] = ''

                if item["company_address"]:
                    item["company_address"] = item["company_address"]
                else:
                    item["company_address"] = ''
                item["company_address"] = self.cw.search_address(item["company_address"])

                yield item

            except:
                return


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "hmw"])