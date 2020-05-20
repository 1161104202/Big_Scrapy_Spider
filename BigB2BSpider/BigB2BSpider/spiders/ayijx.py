# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import BaiChuangHuangYeWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class BaiChuangHuangYeWangSpider(CrawlSpider):
    name = "ayijx"
    allowed_domains = ['www.ayijx.com']
    start_urls = ['http://www.ayijx.com/area/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
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
            allow=r".*", restrict_xpaths=("//div[@class='listsum']//dl//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[@class='dqmqsumxdtb margintop']//li//div[@class='dqmqlefts']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=(
                "//div[@class='navbox']//a[contains(text(),'联系我们')]")),callback='parse_items',follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='fanye']//p//a")),follow=True),

    )

    def parse_items(self, response):
        item = BaiChuangHuangYeWangItem()
        pattern = re.compile(r'<title>联系我们_(.*?)</title>',re.S)
        pattern1 = re.compile(r'<p>电话： (.*?)</p>',re.S)
        pattern2 = re.compile(r'<p>手机： (.*?)</p>', re.S)
        pattern3 = re.compile(r'<p>Q Q： (.*?)</p>', re.S)
        pattern4 = re.compile(r'<p>联系人：(.*?)</p>', re.S)
        pattern5 = re.compile(r'<div class="LOGO_lfont">\s*<p>(.*?)</p>',re.S)

        pattern6 = re.compile(r'>联 系 人：(.*?)<',re.S)
        pattern7 = re.compile(r'> 电    话：(.*?)<', re.S)
        pattern8 = re.compile(r'>手    机： (.*?)<', re.S)
        pattern9 = re.compile(r'> Q    Q：(.*?)<', re.S)
        pattern10 = re.compile(r'>传    真：(.*?)<',re.S)
        pattern11 = re.compile(r'>邮    箱：(.*?)<', re.S)
        pattern12 = re.compile(r'>地    址：(.*?)<', re.S)
        pattern13 = re.compile(r'>企业官网：(.*?)<',re.S)
        pattern14 = re.compile(r'>\s*主营产品：(.*?)<',re.S)

        if response.text is not None:
            try:
                item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
                item["kind"] = "".join(re.findall(pattern14,response.text)) if re.findall(pattern14,response.text) else ''
                item["company_address"] = "".join(re.findall(pattern12,response.text)) if re.findall(pattern12,response.text) else ''
                item["linkman"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
                item["telephone"] = "".join(re.findall(pattern7,response.text)) if re.findall(pattern7,response.text) else ''
                item["phone"] = "".join(re.findall(pattern8,response.text)) if re.findall(pattern8,response.text) else ''
                item["contact_Fax"] = "".join(re.findall(pattern10,response.text)) if re.findall(pattern10,response.text) else ''
                item["contact_QQ"] = "".join(re.findall(pattern9,response.text)) if re.findall(pattern9,response.text) else ''
                item["E_Mail"] = "".join(re.findall(pattern11,response.text)) if re.findall(pattern11,response.text) else ''
                item["Source"] = response.url
                item["province"] = ""
                item["city_name"] = ""

                if item["company_Name"]:
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
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    item["kind"] = item["kind"].replace(' ', '|')
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|').replace('、', '|')\
                        .replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
                else:
                    try:
                        item["kind"] = "|".join(response.xpath("//div[@class='hotico']//ul//li//a//text()").getall())
                        item["kind"] = item["kind"].replace(' ', '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-','|')\
                            .replace('、','|').replace(',', '|').replace('，', '|')\
                            .replace(';', '|').replace('.', '').strip()
                    except:
                        item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
                else:
                    try:
                        item["linkman"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
                    except:
                        item["linkman"] = ''

                if item["linkman"]:
                    if '<' in item["linkman"]:
                        item["linkman"] = item["linkman"].split('<')[0]
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if item["telephone"]:
                    item["telephone"] = item["telephone"]
                else:
                    try:
                        item["telephone"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
                    except:
                        item["telephone"] = ''
                item["telephone"] = self.cw.search_telephone_num(item["telephone"])

                if item["phone"]:
                    item["phone"] = item["phone"]
                else:
                    try:
                        item["phone"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
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
                        item["contact_QQ"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
                    except:
                        item["contact_QQ"] = ''
                item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

                if item["company_address"]:
                    item["company_address"] = self.cw.search_address(item["company_address"])
                else:
                    item["company_address"] = ''

                yield item

            except:
                return


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "ayijx"])