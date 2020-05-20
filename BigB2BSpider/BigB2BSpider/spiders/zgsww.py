# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import ZhongGouShangWuWangspiderItem
from scrapy.cmdline import execute



class ZhongGouShangWuWangSpider(CrawlSpider):
    name = 'zgssw'
    allowed_domains = ['www.shangwuwang.com']
    start_urls = ['http://www.shangwuwang.com/company']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "ASPSESSIONIDQQQBDBAD=PAKPCNLDKGAMHCDLNGBGEPLF; Hm_lvt_539760cac714bd8993dbfb0c1dfb96f7=1564976804; UM_distinctid=16c5fe2f1455-07d6d8162e26fa-5a13331d-1fa400-16c5fe2f14637e; CNZZDATA3636164=cnzz_eid%3D831514679-1564972722-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1564972722; ASPSESSIONIDSQRAAAAC=HEKFDNLDGBDAENAHAMHCLMHJ; Hm_lpvt_539760cac714bd8993dbfb0c1dfb96f7=1564976846",
            # "Host": "www.qy39.com",
            # "Referer": "http://www.qy39.com/beijing-huangye/10",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES' : {
        'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
        # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
    }

    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='content']//div[@class='e_category']//ul//li//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_href:
                print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        li_list = response.xpath("//div[@class='main_left']//ul//li")
        for li in li_list:
            item = ZhongGouShangWuWangspiderItem()
            pattern = re.compile(r'\[(.*?)\/(.*?)\]', re.S)
            item["company_Name"] = li.xpath(".//strong/a/text()").extract_first()
            company_href = li.xpath(".//strong/a/@href").extract_first()
            item["kind"] = li.xpath(".//dd[contains(text(),'主营产品：')]/span/text()").extract_first()
            item["company_address"] = li.xpath(".//dd[contains(text(),'企业地址：')]/text()").extract_first()
            contact_href = li.xpath(".//a[contains(text(),'查看联系方式')]/@href").extract_first()
            if company_href:
                # print(company_href)
                contact_href = "http://www.shangwuwang.com" + contact_href
                # print(contact_href)
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='matpages']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page_url:
            # print(next_page_url)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        item = response.meta["item"]
        # pattern = re.compile(r'<meta name="keywords" content="(.*?)" />',re.S)
        # pattern1 = re.compile(r'<li>主营产品： (.*?)</li>', re.S)
        # pattern2 = re.compile(r'<li>所在地区：(.*?)</li>', re.S)
        # pattern3 = re.compile(r'<li>联系人：(.*?)</li>', re.S)
        # pattern4 = re.compile(r'<li>手机：(.*?)</li>', re.S)
        # pattern5 = re.compile(r'<li>联系电话：(.*?)</li>', re.S)
        # pattern6 = re.compile(r'<li>公司传真：(.*?)</li>', re.S)
        # pattern7 = re.compile(r'href="tencent://message/?Site=jiancai.com&amp;Uin=(.*?)&amp;Menu=yes"',re.S)
        # pattern8 = re.compile(r'>\s*联系人：(.*?)</li>',re.S)

        # item["company_Name"] = response.xpath("//th[contains(text(),'公司名称')]/following-sibling::td//font/text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        item["company_address"] = "".join(response.xpath("//span[contains(text(),'公司地址：')]/../text()").extract())
        item["linkman"] = "".join(response.xpath("//span[contains(text(),'联系人：')]/../text()").extract())
        item["telephone"] = "".join(response.xpath("//span[contains(text(),'电话号码：')]/../text()").extract())
        item["phone"] = "".join(response.xpath("//span[contains(text(),'手机号码：')]/../text()").extract())
        item["E_Mail"] = "".join(response.xpath("//span[contains(text(),'Email地址：')]/following-sibling::strong/a/text()").extract())
        item["contact_Fax"] = item["telephone"]
        item["contact_QQ"] = "".join(response.xpath("//span[contains(text(),'QQ号码：')]/../text()").extract())
        item["province"] = ''
        item["city_name"] = ''
        item["Source"] = response.url

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace('，', '|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"]
        else:
            item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = item["phone"]
        else:
            item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = item["telephone"]
        else:
            item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = item["contact_Fax"]
        else:
            item["contact_Fax"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        if item["E_Mail"]:
            item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        else:
            item["E_Mail"] = ''

        if item["contact_QQ"]:
            item["contact_QQ"] = item["contact_QQ"]
        else:
            item["contact_QQ"] = ''
        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

        if item["company_address"]:
            item["company_address"] = item["company_address"]
        else:
            item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        # if item["host_href"]:
        #     item["host_href"] = item["host_href"]
        # else:
        #     item["host_href"] = ''

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "zgssw"])