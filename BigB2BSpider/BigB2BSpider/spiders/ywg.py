# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.get_md5_hex import get_md5
from BigB2BSpider.items import YiWuGouspiderItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class YiWuGouSpider(CrawlSpider):
    name = "ywg"
    allowed_domains = ['yiwugo.com','www.yiwugo.com','zjzz.yiwugou.com']
    start_urls = ['https://www.yiwugo.com/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
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
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 500,
        }
    }
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='shopsp']//div[@class='index-market-bord']//span//a")), follow=True),

        Rule(LinkExtractor(
            allow=r"\/.*\/.*\.html",restrict_xpaths=("//div[@class='pro_list_product_img2']//li//a")),callback='parse_items', follow=False),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='page_right']//a[contains(text(),'下一页')]")), follow=True),

        # Rule(LinkExtractor(
        #     allow=r".*",restrict_xpaths=("//a[contains(text(),'联系我们')]")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        pattern = re.compile(r'onclick="qqmon\(\'(.*?)\'\)"',re.S)
        item = YiWuGouspiderItem()
        item["company_Name"] = response.xpath("//li[@class='temp-company-v']//span[@class='blod']/text()").extract_first()
        item["company_address"] = response.xpath("//span[contains(text(),'商铺地址：')]/following-sibling::span/text()").extract_first()
        item["linkman"] = response.xpath("//li[@class='c666 ico-shop-01']//span[@class='left']/text()").extract_first()
        item["telephone"] = response.xpath("//li[@class='c666 ico-shop-03']/text()").extract_first()
        item["phone"] = response.xpath("//li[@class='c666 ico-shop-02']/text()").extract_first()
        item["contact_Fax"] = response.xpath("//li[@class='c666 ico-shop-03']/text()").extract_first()
        item["contact_QQ"] = "".join(re.findall(pattern,response.text)[0]) if re.findall(pattern,response.text) else ''
        item["E_Mail"] = response.xpath("//li[@class='c666 ico-shop-04']/text()").extract_first()
        item["kind"] = ",".join(response.xpath("//span[contains(text(),'主营商品：')]/following-sibling::span/text()").extract())
        item["Source"] = response.url
        item["province"] = ''
        item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = item["company_Name"]
        else:
            item["company_Name"] = response.xpath("//div[@class='view_product_bord']//li[@class='f12 fontblue fontbold']/a/@title").get()
        item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(' ','|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace(',', '|').replace('，', '|').replace('.', '|').strip()
        else:
            item["kind"] = response.xpath("//div[@class='fontbluelink mt8px']//a[5]/text()").get()
            item["kind"] = item["kind"].replace(' ', '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace(',', '|').replace('，', '|').replace('.', '|').strip()

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"]
        else:
            item["linkman"] = "".join(response.xpath("//span[contains(text(),'人：')]/following-sibling::span/text()").getall())
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            item["phone"] = response.xpath("//span[contains(text(),'机：')]/following-sibling::span/text()").get()
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            item["telephone"] = response.xpath("//span[contains(text(),'话：')]/following-sibling::span/text()").get()

        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
        else:
            item["contact_Fax"] = item["telephone"]
        if item["contact_Fax"] is None:
            item["contact_Fax"] = ''

        if item["E_Mail"]:
            item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        else:
            item["E_Mail"] = ''

        if item["contact_QQ"]:
            item["contact_QQ"] = item["contact_QQ"]
        else:
            item["contact_QQ"] = ''

        # if item["E_Mail"]:
        #     try:
        #         item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
        #     except:
        #         item["contact_QQ"] = ''
        # else:
        #     item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''


        yield item


if __name__ == '__main__':
    execute(["scrapy", "crawl", "ywg"])