# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import Bigb2BspiderItem
from scrapy.cmdline import execute



class ManfenSpider(CrawlSpider):
    name = 'mfqyw'
    allowed_domains = ['www.mfqyw.com']
    start_urls = ['http://www.mfqyw.com/company/']
    cw = CleanWords()

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            # "Cookie":"Hm_lvt_39b391b010992cf89654d83467db5db7=1564969344; Hm_lpvt_39b391b010992cf89654d83467db5db7=1564970833",
            # "Host":"www.mfqyw.com",
            # "Referer":"http://www.mfqyw.com/",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }

    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='m']//div[@class='left_box']//td//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_name is None:
                kind_name = a.xpath("./strong/text()").extract_first()
            if kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        tr_list = response.xpath("//div[@class='left_box']//div[@class='list']//table//tr")
        for tr in tr_list:
            item = Bigb2BspiderItem()
            pattern = re.compile(r'\[(.*?)\/(.*?)\]', re.S)
            item["company_Name"] = tr.xpath(".//li//a/strong/text()").extract_first()
            company_href = tr.xpath(".//li/a/@href").extract_first()
            item["kind"] = tr.xpath(".//li[contains(text(),'主营：')]/text()").extract_first()
            city_infos = tr.xpath(".//td[@class='f_orange']/text()").extract_first()
            if city_infos:
                # 广东/潮州市
                try:
                    item["province"] = re.findall(pattern, city_infos)[0][0]
                    item["city_name"] = re.findall(pattern, city_infos)[0][1]
                except:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''
            if company_href:
                # print(company_href)
                contact_href = company_href + "contact/"
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='pages']//a[contains(text(),'下一页»')]/@href").extract_first()
        if next_page_url:
            if "http://www.mfqyw.com" in next_page_url:
                next_page_url = next_page_url
            else:
                next_page_url = "http://www.mfqyw.com" + next_page_url
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

        item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        # item["kind"] = response.xpath("//div[@class='head']/h4/text()").extract_first()
        item["company_address"] = "".join(response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/text()").extract())
        item["linkman"] = "".join(response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract())
        item["telephone"] = "".join(response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/text()").extract())
        item["phone"] = "".join(response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/text()").extract())
        item["contact_Fax"] = "".join(response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/text()").extract())
        item["contact_QQ"] = "".join(response.xpath("//td[contains(text(),'即时通讯：')]/following-sibling::td/a/@href").extract())
        item["E_Mail"] = ''
        item["Source"] = response.url

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：', '', item["kind"]).replace('-', '|').replace('、', '|') \
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

        # if item["E_Mail"]:
        #     item["E_Mail"] = self.cw.search_QQ(item["E_Mail"])
        # else:
        #     item["E_Mail"] = ''

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
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
    execute(["scrapy", "crawl", "mfqyw"])