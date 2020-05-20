# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import YiQiYiBiaoJiaoYiWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class YiQiYiBiaoJiaoYiWangSpider(CrawlSpider):
    name = "testmart"
    allowed_domains = ['www.testmart.cn','testmart.cn']
    start_urls = ['http://www.testmart.cn/home/company/index.html']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 420,
        },
    }

    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='fr']//ul[@class='wul']//div[@class='firbox']"
                                         "//div[@class='inul_right']//li//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='left search-Page-right']"
                                          "//div[@class='search-List2']//p[@class='grey weight']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=(
                "//a[contains(text(),'联系我们')]")), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        item = YiQiYiBiaoJiaoYiWangItem()
        pattern = re.compile(r'<a href="javascript:window.external.AddFavorite\(\'.*?\', \'(.*?)\'\)">加入收藏</a>',re.S)
        item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
        item["company_address"] = response.xpath("//li[contains(text(),'地址：')]/text()").extract_first()
        item["linkman"] = response.xpath("//li[contains(text(),'联系人：')]/text()").extract_first()
        item["telephone"] = response.xpath("//li[contains(text(),'电话：')]/text()").extract_first()
        item["phone"] = response.xpath("//li[contains(text(),'手机：')]/text()").extract_first()
        item["contact_Fax"] = response.xpath("//li[contains(text(),'传真：')]/text()").extract_first()
        item["contact_QQ"] = response.xpath("//li[contains(text(),'QQ：')]/a/text()").extract_first()
        item["E_Mail"] = response.xpath("//li[contains(text(),'邮箱：')]/a/text()").extract_first()
        item["Source"] = response.url
        item["kind"] = ",".join(response.xpath("//ul[@class='Wul']//font//text()").getall())
        # city_infos = response.xpath("//li[contains(text(),'地址：')]/text()").get()


        if item["company_Name"] and item["company_Name"] != '':
            if "（" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('（')[0]
            elif "(" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('(')[0]
            elif "_" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('_')[0]
            elif "-" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('-')[0]
            else:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        else:
            return
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(" ", '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            try:
                item["kind"] = ",".join(response.xpath("//div[@class='pkcont_item']//a//text()").getall())
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            except:
                item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"].replace('未填写','')
        else:
            pattern_l = re.compile(r'>联系人:(.*?)<',re.S)
            try:
                item["linkman"] = "".join(re.findall(pattern_l,response.text)[0]) \
                    if re.findall(pattern_l,response.text) else ''
            except:
                item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            pattern_ph = re.compile(r'>手机:(.*?)<', re.S)
            try:
                item["phone"] = "".join(re.findall(pattern_ph,response.text)[0]) \
                    if re.findall(pattern_ph,response.text) else ''
            except:
                item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            pattern_th = re.compile(r'>电话:(.*?)<', re.S)
            try:
                item["telephone"] = "".join(re.findall(pattern_th, response.text)[0]) \
                    if re.findall(pattern_th, response.text) else ''
            except:
                item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
        else:
            pattern_fa = re.compile(r'>传真:(.*?)<', re.S)
            try:
                item["contact_Fax"] = "".join(re.findall(pattern_fa, response.text)[0]) \
                    if re.findall(pattern_fa, response.text) else ''
            except:
                item["contact_Fax"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        if item["E_Mail"]:
            item["E_Mail"] = item["E_Mail"]
        else:
            pattern_em = re.compile(r'>Email:<a href="mailto:.*?">(.*?)<')
            try:
                item["E_Mail"] = response.xpath("//div[@class='mobile_us']//li[contains(text(),'Email：')]/text()").get()
                if item["E_Mail"] is None:
                    try:
                        item["E_Mail"] = "".join(re.findall(pattern_em,response.text)[0]) \
                            if re.findall(pattern_em,response.text) else ''
                    except:
                        item["E_Mail"] = ''
            except:
                item["E_Mail"] = ''
        item["E_Mail"] = self.cw.search_email(item["E_Mail"])

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
        else:
            try:
                item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
            except:
                item["contact_QQ"] = ''
        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

        if item["company_address"]:
            item["company_address"] = item["company_address"]
        else:
            pattern_add = re.compile(r'>地址:(.*?)<', re.S)
            try:
                item["company_address"] = "".join(re.findall(pattern_add, response.text)[0]) \
                    if re.findall(pattern_add, response.text) else ''
            except:
                item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        if item["company_address"]:
            pattern_p = re.compile(r'(.*?)省',re.S)
            pattern_c = re.compile(r'[省](.*?)[市镇县乡区]',re.S)
            try:
                item["province"] = "".join(re.findall(pattern_p,item["company_address"])) \
                    if re.findall(pattern_p,item["company_address"]) else ''
            except:
                item["province"] = ''
            try:
                item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                    if re.findall(pattern_p, item["company_address"]) else ''
            except:
                item["city_name"] = ''
        else:
            item["province"] = ''
            item["city_name"] = ''

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "testmart"])