# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import YiShangWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class YiShangWangSpider(CrawlSpider):
    name = "esw"
    allowed_domains = ['www.esw.com.cn']
    start_urls = ['http://www.esw.com.cn/company/default.aspx?page=1']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
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
            allow=r"\/member\/.*?\.html",restrict_xpaths=("//div[@class='nt_left']//div[@class='yllist']//ul//li//span//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@id='AspNetPager1']//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r"\/member\/contact\d+\.html",
            restrict_xpaths=("///a[contains(text(),'联系我们')]")), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        pattern = re.compile(r'<META name=keywords content=(.*?),.*?>',re.S)
        pattern1 = re.compile(r'<p>\s*联系人：<span id="Span3">(.*?)</span></p>',re.S)
        pattern2 = re.compile(r'<p>\s*手机：<span id="Span2">(.*?)</span></p>',re.S)
        pattern3 = re.compile(r'<p>\s*电话：<span id="x_tel">(.*?)</span></p>',re.S)
        pattern4 = re.compile(r'<p>\s*传真：<span id="x_fax">(.*?)</span></p>',re.S)
        pattern5 = re.compile(r'</p>\s*地址:<span id="x_address">(.*?)<span>',re.S)
        pattern6 = re.compile(r'<META name=keywords content=.*?,(.*?)>', re.S)
        item = YiShangWangItem()
        item["company_Name"] = response.xpath("//div[contains(text(),'公司全称：')]/following-sibling::div/text()").get()
        item["kind"] = response.xpath("//div[contains(text(),'主营业务： ')]/following-sibling::div/text()").get()
        item["company_address"] = response.xpath("//div[contains(text(),'址：')]/following-sibling::div/text()").get()
        item["linkman"] = response.xpath("//div[contains(text(),'联系人')]/following-sibling::div/text()").get()
        item["telephone"] = response.xpath("//div[contains(text(),'话：')]/following-sibling::div/text()").get()
        item["phone"] = response.xpath("//div[contains(text(),'联系人')]/following-sibling::div/text()").get()
        item["contact_Fax"] = response.xpath("//div[contains(text(),'话：')]/following-sibling::div/text()").get()
        item["contact_QQ"] = ''
        item["E_Mail"] = response.xpath("//div[contains(text(),'邮')]/following-sibling::div/a/text()").get()
        item["Source"] = response.url
        item["province"] = ""
        item["city_name"] = ""

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|企 业 名 称：', '', item["company_Name"]).replace(' ', '').strip()
        else:
            try:
                item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|企 业 名 称：', '', item["company_Name"]).replace(' ','').strip()
            except:
                item["company_Name"] = ''
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(' ', '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            try:
                item["kind"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                    .replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            except:
             item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            try:
                # '唐总   13533003050(手机)  '
                item["linkman"] = item["linkman"].split(' ')[0]
            except:
                item["linkman"] = ''
        else:
            try:
                item["linkman"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
            except:
                item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"] and "手机" in item["phone"]:
            pattern = re.compile(r'(\d+)',re.S)
            item["phone"] = re.sub(r'\s|\n|\r|\t','',item["phone"])
            item["phone"] = "".join(re.findall(pattern,item["phone"]))
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            try:
                item["phone"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
            except:
                item["phone"] = ''

        if item["telephone"]:
            try:
                item["telephone"] = item["telephone"].split(' ')[0]
                item["telephone"] = self.cw.search_telephone_num(item["telephone"])
            except:
                item["telephone"] = ''
        else:
            try:
                item["telephone"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
            except:
                item["telephone"] = ''

        if item["contact_Fax"] and "传真：" in item["contact_Fax"]:
            # '020-81633545   传真：020-81633545'
            try:
                item["contact_Fax"] = item["contact_Fax"].split('传真：')[-1]
                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
            except:
                item["contact_Fax"] = ''
        else:
            try:
                item["contact_Fax"] = "".join(re.findall(pattern4, response.text)) if re.findall(pattern4,
                                                                                               response.text) else ''
            except:
                item["contact_Fax"] = ''

        if item["E_Mail"]:
            item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        else:
            item["E_Mail"] = ''

        if item["E_Mail"]:
            item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
        else:
            item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            try:
                item["company_address"] = "".join(re.findall(pattern5, response.text)) if re.findall(pattern5,
                                                                                                 response.text) else ''
            except:
                item["company_address"] = ''

        yield item


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "esw"])