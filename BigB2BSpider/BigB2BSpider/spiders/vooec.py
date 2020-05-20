# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import GuoJiMaoYiWangspiderItem
from scrapy.cmdline import execute



class GuoJiMaoYiWangSpider(CrawlSpider):
    name = 'vooec'
    allowed_domains = ['vooec.com','www.vooec.com','Amis_suntech.cn.vooec.com','jspet_zhang.cn.vooec.com']
    start_urls = ['http://www.vooec.com/company/index.asp']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_34c005d4caf30d75012a05867beca619=1562747829,1564973957; Hm_lpvt_34c005d4caf30d75012a05867beca619=1564974049",
            # "Host": "b2b.huishangbao.com",
            # "Referer": "http://b2b.huishangbao.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }

    def parse(self, response):
        a_list = response.xpath("//table[@class='bottomborder']//table[@class='borderall']//table[2]//tr//table[@class='title']//strong//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_name is None:
                kind_name = a.xpath("./@title").extract_first()
            if kind_href:
                kind_href = "http://www.vooec.com/company/" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_kind_list,
                    dont_filter=True
                )

    def parse_kind_list(self, response):
        a_list = response.xpath("//table[@class='borderall']//td[@bgcolor='#E5E5E5']//table[1]//tr//table[@class='content']//td[@width='90%']//a")
        for a in a_list:
            s_kind_name = a.xpath("./text()").extract_first()
            s_kind_href = a.xpath("./@href").extract_first()
            if s_kind_href:
                s_kind_href = "http://www.vooec.com/company/" + s_kind_href
                yield scrapy.Request(
                    url=s_kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        a_list = response.xpath("//table[8]//td[@class='newscontent']//a")
        for a in a_list:
            item = GuoJiMaoYiWangspiderItem()
            item["company_Name"] = "".join(a.xpath("./strong/text()").extract())
            company_href = a.xpath("./@href").extract_first()
            item["province"] = ''
            item["city_name"] = ''
            if company_href:
                # 'http://xsyr2468.cn.vooec.com/'
                pattern = re.compile(r'http://(.*?).cn.vooec.com/',re.S)
                shop_id = "".join(re.findall(pattern,company_href)) if re.findall(pattern,company_href) else None
                if shop_id:
                    contact_href = company_href + "company_contact_" + shop_id + ".html"
                    # print(company_href,contact_href)
                    if contact_href:
                        yield scrapy.Request(
                            url=contact_href,
                            callback=self.parse_company_contact,
                            meta={"item": item},
                            dont_filter=True
                        )

        next_page_url = response.xpath("//td[@class='content']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page_url:
            next_page_url = "http://www.vooec.com/company/" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        item = response.meta["item"]
        if response.text:
            # item["company_Name"] = response.xpath("//p[contains(text(),'公司名称：')]/text()").extract_first()
            # item["company_address"] = "".join(response.xpath("//p[contains(text(),'地址：')]/text()").extract())
            item["kind"] = response.xpath("//font[contains(text(),'主营业务：')]/text()").extract_first()
            item["linkman"] = response.xpath("//font[contains(text(),'联系人：')]/../following-sibling::td/text()").extract_first()
            item["telephone"] = response.xpath("//font[contains(text(),'话：')]/../following-sibling::td/text()").extract_first()
            item["phone"] = response.xpath("//font[contains(text(),'机：')]/../following-sibling::td/text()").extract_first()
            item["company_address"] = response.xpath("//font[contains(text(),'址：')]/../following-sibling::td/text()").extract_first()
            item["E_Mail"] = ""
            item["contact_Fax"] = response.xpath("//font[contains(text(),'真：')]/../following-sibling::td/text()").extract_first()
            item["contact_QQ"] = ""
            item["Source"] = response.url

            if item["company_Name"]:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|·公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营产品：', '', item["kind"]).replace('-', '|').replace('、', '|') \
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

            yield item


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "vooec"])