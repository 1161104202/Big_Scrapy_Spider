# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import ZaoWaiXinXiWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ZaoWaiXinXiWangSpider(CrawlSpider):
    name = 'zaow'
    allowed_domains = ['www.zaowai.com']
    start_urls = ['http://www.zaowai.com/page/']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Host": "www.yisi.cc",
            # "Referer": "http://www.yisi.cc/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }

    rules = (
        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='dirlist whitebg']//li//div//a")),follow=True),

        Rule(LinkExtractor(
            allow=r"http\:\/\/www\.zaowai\.com\/com\/.*\/",restrict_xpaths=("//div[@id='listcolumn']//li//div[@class='company']//a")), callback='parse_items', follow=True),

        Rule(LinkExtractor(
            allow=r"http\:\/\/www\.zaowai\.com\/guangdong\/pn\d+\/", restrict_xpaths=("//a[contains(text(),'下一页»')]")), follow=True),

        # Rule(LinkExtractor(
        #     allow=r".*",restrict_xpaths=("//div[@id='leftmenu']//a[contains(text(),'联系方式')]")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        item = ZaoWaiXinXiWangItem()
        item["company_Name"] = response.xpath("//div[@class='companyname']/h1/text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        item["kind"] = response.xpath("//div[@class='shop-keyword']/text()").extract_first()
        item["company_address"] = "".join(response.xpath("//li[contains(text(),'公司地址：')]/text()").extract())
        item["linkman"] = "".join(response.xpath("//li[contains(text(),'人：')]/text()").extract())
        item["telephone"] = "".join(response.xpath("//li[contains(text(),'联系电话：')]/text()").extract())
        item["phone"] = ""
        item["contact_Fax"] = "".join(response.xpath("//li[contains(text(),'公司传真：')]/text()").extract())
        item["contact_QQ"] = "".join(response.xpath("//img[@alt='联系QQ']/../@href").extract())
        item["E_Mail"] = "".join(response.xpath("//li[contains(text(),'电子邮箱：')]/text()").extract())
        item["Source"] = response.url
        item["province"] = ''
        item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(' ','|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace(',', '|').replace(';','|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = re.sub(r'\s|\n|\r|\t','',item["linkman"])
            item["linkman"] = item["linkman"].replace("联系人：","")
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
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "zaow"])