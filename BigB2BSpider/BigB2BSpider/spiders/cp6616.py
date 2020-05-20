# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import ChangPinLiuLiuYiLiuspiderItem
from scrapy.cmdline import execute



class ChangPinLiuLiuYiLiuSpider(CrawlSpider):
    name = 'cp6616'
    allowed_domains = ['www.cp6616.com']
    start_urls = ['http://www.cp6616.com/company/index.aspx']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
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
        a_list = response.xpath("//div[@class='all-sort-list']//div[@class='item']//h3//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_href:
                if kind_href.startswith("http://"):
                    kind_href = kind_href
                else:
                    kind_href = "http://www.cp6616.com" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        div_list = response.xpath("//div[@class='product_list']//div[contains(@class,'left_item')]")
        for div in div_list:
            item = ChangPinLiuLiuYiLiuspiderItem()
            pattern = re.compile(r'所在地区：(.*?)省(.*?)市', re.DOTALL)
            item["company_Name"] = div.xpath(".//div[@class='trade_info_name']/a/text()").extract_first()
            company_href = div.xpath(".//div[@class='trade_info_name']/a/@href").extract_first()
            item["kind"] = div.xpath(".//div[contains(text(),'主营产品：')]/text()").extract_first()
            city_infos = div.xpath(".//p[contains(text(),'所在地区：')]/text()").extract_first()
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
                contact_href = company_href + "Contact.html"
                # print(contact_href)
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='pages']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page_url:
            next_page_url = "http://www.cp6616.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        item = response.meta["item"]
        item["company_Name"] = response.xpath("//li[contains(text(),'·公司名称：')]/text()").extract_first()
        item["company_address"] = "".join(response.xpath("//li[contains(text(),'·公司地址：')]/text()").extract())
        item["linkman"] = "".join(response.xpath("//li[contains(text(),'·联系人：')]/text()").extract())
        item["telephone"] = "".join(response.xpath("//li[contains(text(),'·联系电话：')]/text()").extract())
        item["phone"] = "".join(response.xpath("//li[contains(text(),'·联系手机：')]/text()").extract())
        item["E_Mail"] = response.xpath("//li[contains(text(),'·电子邮件：')]/text()").extract_first()
        item["contact_Fax"] = ''
        item["contact_QQ"] = "".join(response.xpath("//li[contains(text(),'·QQ号：')]/text()").extract())
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
    execute(["scrapy", "crawl", "cp6616"])