# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import ShangQuWangspiderItem
from scrapy.cmdline import execute



class ShangQuWang(CrawlSpider):
    name = 'salqu'
    allowed_domains = ['www.salqu.com']
    start_urls = ['http://www.salqu.com/company/']
    cw = CleanWords()

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "PHPSESSID=gluoteaio8b0brt17o9msoqa14",
            # "Host": "www.salqu.com",
            # "Referer": "http://www.salqu.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='col-xs-12']//dd[@class='place']//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        div_list = response.xpath("//div[@id='list']//div[@class='company-wrap']")
        for div in div_list:
            item = ShangQuWangspiderItem()
            # pattern = re.compile(r'(.*?)\/(.*?)', re.S)
            item["company_Name"] = div.xpath(".//span[@class='company-name']/a/text()").extract_first()
            company_href = div.xpath(".//span[@class='company-name']/a/@href").extract_first()
            item["kind"] = div.xpath(".//span[contains(text(),'主营产品：')]/text()").extract_first()
            city_infos = div.xpath(".//p[contains(text(),'所在地区')]/following-sibling::p/text()").extract_first()
            if city_infos:
                # 广东/潮州市
                try:
                    item["province"] = city_infos.split("/")[0]
                    item["city_name"] = city_infos.split("/")[1]
                except:
                    item["province"] = city_infos
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''
            if company_href:
                # print(company_href)
                contact_href = company_href + "contact/"
                # print(contact_href)
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='pages']//a[contains(text(),'下一页»')]/@href").extract_first()
        if next_page_url:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "PHPSESSID=gluoteaio8b0brt17o9msoqa14",
            # "Host": "xyblifei.salqu.com",
            "Referer": response.url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }
        item = response.meta["item"]
        item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        # item["kind"] = response.xpath("//div[@class='head']/h4/text()").extract_first()
        item["company_address"] = "".join(response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/a/text()").extract())
        item["linkman"] = "".join(response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract())
        item["telephone"] = "".join(response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/img/@src").extract())
        item["phone"] = "".join(response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/img/@src").extract())
        item["E_Mail"] = "".join(response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/img/@src").extract())
        item["contact_Fax"] = "".join(response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/img/@src").extract())
        item["contact_QQ"] = "".join(response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract())
        item["Source"] = response.url

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
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
            item["phone"] = self.requests_href(item["phone"], headers)
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            item["phone"] = ''

        if item["telephone"]:
            item["telephone"] = self.requests_href(item["telephone"], headers)
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            item["telephone"] = ''

        if item["contact_Fax"]:
            item["contact_Fax"] = self.requests_href(item["contact_Fax"], headers)
            item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
        else:
            item["contact_Fax"] = ''

        if item["E_Mail"]:
            item["E_Mail"] = self.requests_href(item["E_Mail"], headers)
            if item["E_Mail"]:
                item["E_Mail"] = item["E_Mail"].replace("e", "@").replace("8126", "@163").replace("8163", "@163").strip()
            # item["E_Mail"] = self.cw.search_email(item["E_Mail"])
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

        # if item["host_href"]:
        #     item["host_href"] = item["host_href"]
        # else:
        #     item["host_href"] = ''

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
            something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img\image.png"
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
    execute(["scrapy", "crawl", "salqu"])