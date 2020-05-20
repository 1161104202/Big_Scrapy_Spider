# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import KuSoBaspiderItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class KuSoBaSpider(CrawlSpider):
    name = "ksb"
    allowed_domains = ['www.kusoba.com']
    start_urls = ['http://www.kusoba.com/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
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
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r"/.*/",restrict_xpaths=("//div[@class='beij_center']//div[@class='wenzlieb']//a")), follow=True),

        Rule(LinkExtractor(
            allow=r"/company/\d+.html", restrict_xpaths=("//div[@class='beij_center']//div[@class='nianmf']//a")),
            callback='parse_items', follow=False),

        Rule(LinkExtractor(allow=r"/.*/p.*/", restrict_xpaths=("//div[@class='fanye']//a")), follow=True),
    )

    def parse_items(self, response):
        # print(response.text)
        pattern = re.compile(r'<li><p>联系我们：</p><span>(.*?)</span></li>',re.S)
        pattern1 = re.compile(r'<li><p>电<em></em>话：</p><span>(.*?)</span></li>', re.S)
        pattern2 = re.compile(r'<li><p>移动电话：</p><span>(.*?)</span></li>', re.S)
        pattern3 = re.compile(r'<li><p>传<em></em>真：</p><span>(.*?)</span></li>', re.S)
        item = KuSoBaspiderItem()
        item["company_Name"] = "".join(response.xpath("//div[contains(text(),'全称：')]/text()").extract())
        item["kind"] = "".join(response.xpath("//div[contains(text(),'主营产品：')]/text()").extract())
        item["company_address"] = "".join(response.xpath("//div[contains(text(),'注册地址：')]/text()").extract())
        item["linkman"] = "".join(response.xpath("//div[contains(text(),'法定代表人：')]/text()").extract())
        item["telephone"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
        item["phone"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
        item["contact_Fax"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
        item["contact_QQ"] = ""
        item["E_Mail"] = ""
        item["Source"] = response.url
        item["province"] = ""
        item["city_name"] = ""

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|全称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营产品：', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace('，', '|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            if "（" in item["linkman"]:
                item["linkman"] = item["linkman"].split("（")[0].replace('法定代表人：','').replace('暂未公布','')
            else:
                item["linkman"] = item["linkman"].replace('法定代表人：','').replace('暂未公布','')
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
            item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = item["company_address"].replace('注册地址：','')
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "ksb"])