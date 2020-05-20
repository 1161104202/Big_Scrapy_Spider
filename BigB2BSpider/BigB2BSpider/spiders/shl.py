# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import ShangLuWangspiderItem
from scrapy.cmdline import execute




class ShangLuWang(CrawlSpider):
    name = 'shl'
    allowed_domains = ['www.b2b6.com']
    start_urls = ['http://www.b2b6.com']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "__jsluid_h=5ce7ed337548f20c7a26c70933fc9b8a; UM_distinctid=16c6b51bdb62b1-0f185a00dd70c9-5a13331d-1fa400-16c6b51bdb7460; CNZZDATA4872360=cnzz_eid%3D973033440-1565166565-http%253A%252F%252Fwww.b2b6.com%252F%26ntime%3D1565166565",
            # "Host": "www.b2b6.com",
            # "Referer": "http://www.b2b6.com/yp/h1f3s0c0p10.aspx",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }

    def parse(self, response):
        a_list = response.xpath("//div[@id='dMain']//div[@class='mt']//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_href:
                kind_href = "http://www.b2b6.com" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_kind_list,
                    dont_filter=True
                )
    def parse_kind_list(self, response):
        a_list = response.xpath("//div[@id='dMain']//div[@id='dCatalogueBox']//ul//li//a")
        for a in a_list:
            # item["kind"] = a.xpath("./@title").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_href:
                # print(item["kind"],kind_href)
                kind_href = "http://www.b2b6.com" + kind_href
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        kinds = "".join(response.xpath("//div[@id='dNavBox']//a[contains(text(),'首页')]/..//text()").extract())
        # if kinds and "市" in kinds:
        #     try:
        #         # '商录分享目录首页 > 天津市 > 综合性行业'
        #         kinds = re.sub(r'\s|\n|r|\t','',kinds).replace(' ','')
        #         kinds = kinds.split('市>')[-1]
        #     except:
        #         kinds = ''
        # else:
        #     kinds = ''
        div_list = response.xpath("//div[@id='dMain']//div[@id='dMainBox']")
        for div in div_list:
            item = ShangLuWangspiderItem()
            # pattern = re.compile(r'(.*?)\/(.*?)', re.S)
            item["company_Name"] = div.xpath(".//a/text()").extract_first()
            item["company_address"] = div.xpath(".//span[@class='addr']/text()").extract_first()
            company_href = div.xpath(".//a/@href").extract_first()
            item["province"] = ''
            item["city_name"] = ''
            item["kind"] = ''
            if company_href:
                # print(company_href)
                contact_href = "http://www.b2b6.com" + company_href
                # print(contact_href)
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@id='dMain']//div[@id='dMainBox']//b[contains(text(),'下一页')]/../@href").extract_first()
        if next_page_url:
            next_page_url = "http://www.b2b6.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        item = response.meta["item"]
        pattern = re.compile(r'<b>公司名称： </b> (.*?)<br />',re.S)
        pattern1 = re.compile(r'<b>联系电话：</b> (.*?)<br />', re.S)
        pattern2 = re.compile(r'<b>公司地址：</b> (.*?)<br />', re.S)
        pattern3 = re.compile(r'<b>经营范围：</b> (.*?)<br />', re.S)
        pattern4 = re.compile(r'<b>网站网址：</b> <a  target=_blank  href=".*?" >(.*?)</a><br />', re.S)
        pattern5 = re.compile(r'<b>经济行业：</b> <a href=.*?>(.*?)</a><br />',re.S)

        item["company_Name"] = "".join(re.findall(pattern,response.text)) if response.text else ''
        item["company_address"] = "".join(re.findall(pattern2,response.text)) if response.text else ''
        item["linkman"] = ''
        item["telephone"] = "".join(re.findall(pattern1,response.text)) if response.text else ''
        item["phone"] = ''
        item["E_Mail"] = ''
        item["contact_Fax"] = ''
        item["contact_QQ"] = ''
        item["Source"] = response.url
        kinds = response.xpath("//div[@id='dNavBox']/div/a[3]/text()").extract_first()

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:

            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace('，', '|').replace('.', '').strip().lstrip('|')
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(kinds))
        if item["kind"]:
            try:
                item["kind"] = item["kind"].split('</')[0]
            except:
                item["kind"] = ''
        else:
            item["kind"] = ''

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
            item["E_Mail"] = item["E_Mail"]
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
    execute(["scrapy", "crawl", "shl"])