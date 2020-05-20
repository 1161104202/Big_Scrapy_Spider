# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import ShangMingLuWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ShangMingLuWangSpider(CrawlSpider):
    name = "sml_v1"
    allowed_domains = ['www.b2bname.com']
    start_urls = ['http://www.b2bname.com/area.php']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
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

    def parse(self, response):
        div_list = response.xpath("//div[@class='main mgline']//dl[@id='alllist']//dd//a")
        for div in div_list:
            city_href = div.xpath("./@href").get()
            city_name = div.xpath("./text()").get()
            if city_href:
                # print(city_name,city_href)
                yield scrapy.Request(
                    url=city_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        a_list = response.xpath("//div[@class='main mgline']//div[@class='block-tab-item mgline']//ul//li")
        for a in a_list:
            company_Name = a.xpath(".//a/text()").get()
            company_href = a.xpath(".//a/@href").get()
            kind = a.xpath(".//a/../following-sibling::span/text()").get()
            if company_href:
                # print(company_Name,company_href)
                yield scrapy.Request(
                    url=company_href,
                    callback=self.parse_company_detail,
                    meta={"info": kind},
                    dont_filter=True
                )

        next_page_url = response.xpath("//b[contains(text(),'下一页')]/../@href").get()
        if next_page_url:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_detail(self, response):
        kind = response.meta.get("info")
        contact_href = response.xpath("//a[contains(text(),'联系方式')]/@href").get()
        if contact_href:
            yield scrapy.Request(
                url=contact_href,
                callback=self.parse_company_contact,
                meta={"info":kind},
                dont_filter=True
            )

    def parse_company_contact(self, response):
        item = ShangMingLuWangItem()
        pattern = re.compile(r'(1\d{10})', re.S)
        pattern1 = re.compile(r'<meta name="keywords" content=".*?_.*?;(.*?)"/>',re.S)
        item["company_Name"] = response.xpath("//b[contains(text(),'单位名称:')]/../text()").extract_first()
        item["kind"] = response.meta.get("info")
        item["company_address"] = response.xpath("//b[contains(text(),'地址:')]/../text()").extract_first()
        item["linkman"] = response.xpath("//b[contains(text(),'联系人:')]/../text()").extract_first()
        item["telephone"] = ''
        item["phone"] = "".join(re.findall(pattern,response.text)[0]) if re.findall(pattern,response.text) else ''
        item["contact_Fax"] = response.xpath("//b[contains(text(),'传真:')]/../text()").extract_first()
        item["contact_QQ"] = response.xpath("//b[contains(text(),'QQ:')]/../text()").extract_first()
        item["E_Mail"] = response.xpath("//b[contains(text(),'邮箱:')]/../text()").extract_first()
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
            item["kind"] = "|".join(re.findall(pattern1,response.text)[0]) if re.findall(pattern1,response.text) else ''
            item["kind"] = item["kind"].replace(' ', '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            if re.findall(r'(1\d+)', item["linkman"]):
                try:
                    item["linkman"] = re.sub("".join(re.findall(r'(1\d+)', item["linkman"])),'',item["linkman"])
                except:
                    item["linkman"] = ''
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
    execute(["scrapy", "crawl", "sml_v1"])