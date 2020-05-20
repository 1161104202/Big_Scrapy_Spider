# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import CebnDianZiShangWuWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute


class CebnDianZiShangWuWangSpider(CrawlSpider):
    name = "cebn"
    allowed_domains = ['www.cebn.cn','cebn.cn']
    start_urls = ['http://www.cebn.cn/company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Host": "www.kusoba.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='fl J-mainNav']//ul//li//a")), follow=True),

        Rule(LinkExtractor(allow=r".*",restrict_xpaths=("//div[@class='list-content']//div[@class='proname']//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='pages']//a[contains(text(),'下一页»')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//span[contains(text(),'联系方式')]/..")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "UM_distinctid=16cb2979f862a5-0dfda36ee0202d-5a13331d-1fa400-16cb2979f8725e; Hm_lvt_aa1b57052b9004f48376724837cc9b69=1566364377; yunsuo_session_verify=ded7c3ded7b4429e61379b82e2e37d8e; Hm_lpvt_aa1b57052b9004f48376724837cc9b69=1566365005",
            # "Host": "fshjbxg.cn.cebn.cn",
            "Referer": response.url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }
        item = CebnDianZiShangWuWangItem()
        if response.text:
            try:
                item["company_Name"] = response.xpath(
                    "//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
                item["kind"] = response.xpath("//div[@class='head']//h4/text()").get()
                item["company_address"] = "".join(
                    response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/text()").extract())
                item["linkman"] = response.xpath(
                    "//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract_first()
                item["telephone"] = response.xpath(
                    "//td[contains(text(),'公司电话：')]/following-sibling::td/img/@src").extract_first()
                item["phone"] = response.xpath(
                    "//td[contains(text(),'手机号码：')]/following-sibling::td/img/@src").extract_first()
                item["contact_Fax"] = response.xpath(
                    "//td[contains(text(),'公司传真：')]/following-sibling::td/img/@src").extract_first()
                item["contact_QQ"] = response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract_first()
                item["E_Mail"] = response.xpath(
                    "//td[contains(text(),'电子邮件：')]/following-sibling::td/img/@src").extract_first()
                item["Source"] = response.url
                item["province"] = ""
                item["city_name"] = ""

                if item["company_Name"]:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|全称：', '', item["company_Name"]).replace(' ', '').strip()
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    item["kind"] = item["kind"].replace(" ", "|")
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营产品：', '', item["kind"]).replace('-', '|').replace('、', '|') \
                        .replace('，', '|').replace('，', '|').replace('.', '').strip()
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    if "（" in item["linkman"]:
                        item["linkman"] = item["linkman"].split("（")[0].replace('法定代表人：','').replace('暂未公布','')
                    else:
                        item["linkman"] = item["linkman"].replace('法定代表人：','').replace('暂未公布','')
                else:
                    item["linkman"] = ''
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if item["phone"]:
                    item["phone"] = self.requests_href(item["phone"], headers)
                    item["phone"] = self.cw.search_phone_num(item["phone"])
                else:
                    item["phone"] = ''

                if item["telephone"]:
                    item["telephone"] = self.requests_href(item["telephone"],headers)
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
                    item["E_Mail"] = self.cw.search_email(item["E_Mail"])
                else:
                    item["E_Mail"] = ''

                if item["contact_QQ"]:
                    # item["contact_QQ"] = self.requests_href(item["contact_QQ"], headers)
                    item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
                else:
                    item["contact_QQ"] = ''

                if item["company_address"]:
                    # if "\"" in item["company_address"]:
                    item["company_address"] = item["company_address"]
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

    def requests_href(self, url, headers):
        res = requests.get(url=url, headers=headers, timeout=10, verify=False)
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
    execute(["scrapy", "crawl", "cebn"])