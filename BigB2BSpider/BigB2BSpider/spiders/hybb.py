# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.get_md5_hex import get_md5
from BigB2BSpider.items import HuangYeBaBaItem
from BigB2BSpider.data_tools.orc_img import recognition_image
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class HuangYeBaBaSpider(CrawlSpider):
    name = "hybb"
    allowed_domains = ['huangye88.com','b2b.huangye88.com']
    start_urls = ['http://b2b.huangye88.com/']
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
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 500,
        }
    }

    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='sider']//div[@class='box hot_cp'][2]//div[@class='ad_list']//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='main']//div[@class='tag_tx']//ul//li//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='box']//form[@name='jubao']//dl//h4//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='page_tag Baidu_paging_indicator']//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//li[contains(text(),'联系我们')]/..")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        item = HuangYeBaBaItem()
        item["company_Name"] = response.xpath("//div[@class='big']/div/text()").extract_first()
        item["company_address"] = response.xpath("//label[contains(text(),'地址：')]/../text()").extract_first()
        item["linkman"] = "".join(response.xpath("//div[@class='site']//label[contains(text(),'联系人：')]/..//text()").extract())
        item["telephone"] = response.xpath("//div[@class='site']//label[contains(text(),'电话：')]/../text()").extract_first()
        item["phone"] = response.xpath("//div[@class='site']//label[contains(text(),'手机：')]/../text()").extract_first()
        item["contact_Fax"] = response.xpath("//div[@class='site']//label[contains(text(),'传真：')]/../text()").extract_first()
        item["contact_QQ"] = ''
        item["E_Mail"] = ''
        item["Source"] = response.url
        item["kind"] = "".join(response.xpath("//dt[contains(text(),'主营产品')]/following-sibling::dd/text()").getall())
        item["province"] = ''
        item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = item["company_Name"]
        else:
            item["company_Name"] = response.xpath("//label[contains(text(),'公司名称：')]/../text()").get()

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(" ",'|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace(' ', '|').replace('-', '|') \
                .replace('、', '|').replace(';','|').replace('_','|').replace('，', '|').replace(',', '|').replace('.', '|').strip()
        else:
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
    execute(["scrapy", "crawl", "hybb"])