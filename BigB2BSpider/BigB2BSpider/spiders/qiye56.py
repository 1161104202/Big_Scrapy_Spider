# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import QiYeWuLiuspiderItem
from BigB2BSpider.data_tools.orc_img import recognition_image
from scrapy.cmdline import execute



class QiYeWuLiuSpider(CrawlSpider):
    name = 'qy56'
    allowed_domains = ['www.56ye.net','qiye.56ye.net']
    start_urls = ['http://qiye.56ye.net/']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
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
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }

    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='m']//div[@class='m_q f_l']//div[@class='qys']//td//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_name is None:
                kind_name = a.xpath("./strong/span[1]/text()").extract_first()
            if kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        kind = response.xpath("//div[@class='pos_3']//a[2]/text()").extract_first()
        tr_list = response.xpath("//div[@class='m']//div[@class='list']//table//tr")
        for tr in tr_list:
            item = QiYeWuLiuspiderItem()
            # pattern = re.compile(r'\[(.*?)\/(.*?)\]', re.S)
            item["company_Name"] = tr.xpath(".//li//a/text()").extract_first()
            item["company_id"] = self.get_md5(item["company_Name"])
            item["company_address"] = tr.xpath("//li[contains(text(),'公司地址：')]/text()").extract_first()
            company_href = tr.xpath(".//li/a/@href").extract_first()
            item["kind"] = kind
            item["linkman"] = ''
            item["contact_Fax"] = ''
            item["contact_QQ"] = ''
            item["E_Mail"] = ''
            item["Source"] = response.url
            contact_infos = tr.xpath(".//li[@class='tel']/text()").extract_first()
            # city_infos = tr.xpath(".//td[@class='f_orange']/text()").extract_first()
            if contact_infos:
                item["phone"] = self.cw.search_phone_num(contact_infos)
                item["telephone"] = self.cw.search_telephone_num(contact_infos)
            else:
                item["phone"] = ''
                item["telephone"] = ''
            if item["company_address"]:
                item["company_address"] = self.cw.search_address(item["company_address"])
            else:
                item["company_address"] = ''
            item["province"] = ''
            item["city_name"] = ''

            if company_href:
                # print(company_href)
                contact_href = company_href + "contact/"
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={
                        "item": item,
                        "info1": kind
                    },
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='pages']//a[contains(text(),'下一页»')]/@href").extract_first()
        if next_page_url:
            if next_page_url.startswith("http://"):
                next_page_url = next_page_url
            else:
                next_page_url = "http://qiye.56ye.net" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        item = response.meta["item"]
        if "公司主页正在等待开通" in response.text:
            yield item
        else:
            item = response.meta["item"]
            item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
            item["company_address"] = "".join(response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/text()").extract())
            item["linkman"] = response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract_first()
            item["telephone"] = response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/text()").extract_first()
            item["phone"] = response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/text()").extract_first()
            item["contact_Fax"] = response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/text()").extract_first()
            item["contact_QQ"] = response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract_first()
            item["E_Mail"] = response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/text()").extract_first()
            item["Source"] = response.url

            if item["company_Name"]:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                    .replace('，', '|').replace('，', '|').replace('.', '').strip()
            else:
                item["kind"] = response.meta.get("info1")

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

    def requests_href(self, url, headers):
        res = requests.get(url=url, headers=headers, timeout=20, verify=False)
        res.encoding = "utf-8"
        if res.status_code == requests.codes.ok:
            img = res.content
            something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img1\image.png"
            with open(something_img_file_path, "wb") as fp:
                fp.write(img)
            fp.close()
            if img:
                try:
                    something = recognition_image(something_img_file_path)
                    if something:
                        return something
                    else:
                        return ''
                except:
                    return ''
            else:
                return ''
        else:
            return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "qy56"])