# -*- coding: utf-8 -*-
import re
import scrapy
import requests
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import RouDianGongChengspiderItem
from scrapy.cmdline import execute



class RouDianGongChengSpider(CrawlSpider):
    name = 'rdgc'
    allowed_domains = ['rdzjw.com','www.rdzjw.com']
    start_urls = ['http://www.rdzjw.com/company/']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_081b84205c0f16480d7a8964a70f6b6b=1565055009; BAIDU_SSP_lcr=http://hao.huangye88.com/b2b_42621.html; Hm_lpvt_081b84205c0f16480d7a8964a70f6b6b=1565055034",
            # "Host": "www.fashangji.com",
            # "Referer": "https://www.fashangji.com/",
            # "Sec-Fetch-Mode": "navigate",
            # "Sec-Fetch-Site": "none",
            # "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
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
                print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        div_list = response.xpath("//div[@class='m']//div[@class='list']//table//tr")
        for div in div_list:
            item = RouDianGongChengspiderItem()
            # pattern = re.compile(r'\[\(.*?\)\/\(.*?\)\]', re.S)
            item["company_Name"] = div.xpath(".//td[@align='left']//li/a/strong/text()").extract_first()
            company_href = div.xpath(".//td[@align='left']//li/a/@href").extract_first()
            item["kind"] = div.xpath(".//td[@align='left']//li[contains(text(),'主营：')]/text()").extract_first()
            city_infos = "".join(div.xpath("//td[@align='left']/following-sibling::td/text()").extract_first())

            if city_infos and "/" in city_infos:
                # 广东/潮州市
                try:
                    item["province"] = city_infos.replace("[", '').replace("]", '').split('/')[0]
                    item["city_name"] = city_infos.replace("[", '').replace("]", '').split('/')[-1]
                except:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = city_infos.replace("[", '').replace("]", '')
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
            "Cookie": "URnU_6599_saltkey=ak6gp656; URnU_6599_lastvisit=1565058750; BAIDU_SSP_lcr=https://www.baidu.com/link?url=cb-lCyEOCCLgFwHPL2dAanIBMLf8DvDyItiG2Ov4tBa&wd=&eqid=9f23e6d6000403b3000000065d48f4ac; UM_distinctid=16c64fc50e79b-0e9495f2b9b774-5a13331d-1fa400-16c64fc50e868; CNZZDATA1254919241=1514860467-1565058564-null%7C1565058564; URnU_6599_lastact=1565062639%09api.php%09js",
            "Host": "www.rdzjw.com",
            "Referer": response.url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }
        item = response.meta["item"]
        item["company_Name"] = response.xpath(
            "//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        # item["kind"] = response.xpath("//div[@class='head']/h4/text()").extract_first()
        item["company_address"] = "".join(
            response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/text()").extract())
        item["linkman"] = "".join(
            response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract())
        item["telephone"] = "".join(
            response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/img/@src").extract())
        item["phone"] = "".join(
            response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/img/@src").extract())
        item["contact_Fax"] = "".join(
            response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/text()").extract())
        item["contact_QQ"] = "".join(response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract())
        item["E_Mail"] = "".join(
            response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/img/@src").extract())
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
                item["E_Mail"] = item["E_Mail"].replace("e", "@").replace("8126", "@126").replace("8163",
                                                                                                  "@163").strip()
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
            something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img2\image.png"
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
    execute(["scrapy", "crawl", "rdgc"])