# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import WanYouYinLiShangMaoWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class WanYouYinLiShangMaoWangSpider(CrawlSpider):
    name = 'any2000'
    allowed_domains = ['gs.any2000.com','cn.any2000.com']
    start_urls = ['http://gs.any2000.com/']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.8,
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
            allow=r".*", restrict_xpaths=("//div[@class='left f_l']//div[@class='gys_content']//div[@class='qys_pro_nr']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@id='gysp-n']//div[@class='gysp-n_list']//ul//strong/..")), callback='parse_items', follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='pages']//a[contains(text(),'下一页')]")), follow=True),

        # Rule(LinkExtractor(
            # allow=r".*",restrict_xpaths=("//nav[@class='menu']//a[contains(text(),'联系我们')]")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        item = WanYouYinLiShangMaoWangItem()
        pattern = re.compile(r'<div id="logo">(.*?)</div>',re.S)
        pattern1 = re.compile(r'<meta name="keywords" content=".*?,(.*?)"/>',re.S)
        pattern2 = re.compile(r'<p>主营：(.*?)</p>',re.S)
        pattern3 = re.compile(r'>\s*公司地址：(.*?)<',re.S)
        pattern4 = re.compile(r'>\s*联 系 人：(.*?)<',re.S)
        pattern5 = re.compile(r'>\s*电话：(.*?)<', re.S)
        pattern6 = re.compile(r'>\s*公司传真：(.*?)<', re.S)
        pattern7 = re.compile(r'>\s*主营行业：(.*?)    <', re.S)
        item["company_Name"] = response.xpath("//div[@id='logo']/text()").get()
        # item["company_Name"] = response.xpath("//div[@class='companyname']//td[2]//text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        item["kind"] = response.xpath("//div[@id='logo_wz']//p[contains(text(),'主营：')]").get()
        item["company_address"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
        item["linkman"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
        item["telephone"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
        item["phone"] = ""
        item["contact_Fax"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
        item["contact_QQ"] = ""
        item["E_Mail"] = ""
        item["Source"] = response.url
        item["province"] = ''
        item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        else:
            item["company_Name"] = response.xpath("//div[@id='logo_wz']//strong/text()").get()
            if item["company_Name"]:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(' ','|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace(',', '|').replace(';','|').replace('.', '').strip()
        else:
            try:
                item["kind"] = ",".join(re.findall(pattern7,response.text)) if re.findall(pattern7,response.text) else ''
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                    .replace('，', '|').replace(',', '|').replace(';', '|').replace('.', '').strip()
            except:
                item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = re.sub(r'\s|\n|\r|\t|未填写','',item["linkman"])
        # else:
        #     item["linkman"] = response.xpath("//p[contains(text(),'联 系 人  ：  ')]//i/text()").get()
        #     item["linkman"] = re.sub(r'\s|\n|\r|\t|未填写', '', item["linkman"])
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
            item["company_address"] = item["company_address"]
        else:
            item["company_address"] = "".join(response.xpath("//p[contains(text(),'详细地址：')]//text()").getall())
        item["company_address"] = self.cw.search_address(item["company_address"])

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "any2000"])