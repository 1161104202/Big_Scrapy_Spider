# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import MingZhanZaiXianItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class MingZhanZaiXianSpider(CrawlSpider):
    name = "fwol"
    # allowed_domains = ['www.53info.com','qineng1688.53info.com']
    start_urls = ['http://www.fwol.cn/company.php']
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
        "DOWNLOAD_HANDLERS_BASE": {
            'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
            'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        },
        # "DOWNLOAD_HANDLERS": {
        #     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'},
    }
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//table[7]//table//nobr//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//table[7]//table[@bgcolor='#CCCCCC']//tr[@bgcolor='#f0f0f0']//td[2]//a")), callback='parse_items',follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//a[contains(text(),'下一页')]")), follow=False),

    #     Rule(LinkExtractor(
    #         allow=r".*",restrict_xpaths=("//div[@id='nav']//a[contains(text(),'联系我们')]")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        pattern = re.compile(r'>公司名称：(.*?) <', re.S)
        pattern1 = re.compile(r'>电　　话：(.*?)<', re.S)
        pattern2 = re.compile(r'>传　　真：(.*?)<', re.S)
        pattern3 = re.compile(r'>地　　址：(.*?)<', re.S)
        pattern4 = re.compile(r'>联　　系：(.*?)<', re.S)
        pattern5 = re.compile(r'>电子邮箱：<a href=".*?">(.*?)<', re.S)
        pattern6 = re.compile(r'别：<a href=".*?" target=_blank>.*?</a> <a href=".*?" target="_blank">(.*?)<', re.S)

        item = MingZhanZaiXianItem()
        contact_infos = ",".join(response.xpath("//div[@class='contact']//div[@class='item']//span").getall())
        item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
        item["kind"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
        item["company_address"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
        item["linkman"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
        item["telephone"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
        item["phone"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
        item["contact_Fax"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
        item["contact_QQ"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
        item["E_Mail"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
        item["Source"] = response.url
        item["province"] = ''
        item["city_name"] = ''

        if item["company_Name"]:
            if "<br>" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('<br>')[0]
            else:
                item["company_Name"] = item["company_Name"]
        item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(' ', '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|未分类', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace(',', '|').replace('，', '|').replace('.', '').strip()
        else:
            # try:
            #     item["kind"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
            #     item["kind"] = item["kind"].replace(' ', '|')
            #     item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
            #         .replace(',', '|').replace('，', '|').replace('.', '').strip()
            # except:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            pattern7 = re.compile(r'\d+',re.S)
            num = "".join(re.findall(pattern7,item["linkman"].strip()))
            if num:
                item["linkman"] = ''
        else:
            item["linkman"] = self.cw.search_linkman(item["linkman"])

        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            try:
                item["phone"] = self.cw.search_phone_num(contact_infos)
            except:
                item["phone"] = ''

        if item["telephone"]:
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            try:
                item["telephone"] = self.cw.search_telephone_num(contact_infos)
            except:
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
            item["contact_QQ"] = ''

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
    execute(["scrapy", "crawl", "fwol"])