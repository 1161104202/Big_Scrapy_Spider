# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import DianQiZiDongHuaWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class DianQiZiDongHuaWangSpider(CrawlSpider):
    name = "eachina"
    allowed_domains = ['www.ea-china.com','a-china.com']
    start_urls = ['http://www.ea-china.com/company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
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
    # //span[contains(text(),'企业分类')]/../../../../../../following-sibling::tr//tr//td//a
    rules = (
        Rule(LinkExtractor(
            allow=r"more.asp\?sortid=\d+",restrict_xpaths=("//tr//td//a")),follow=True),

        Rule(LinkExtractor(
            allow=r"info.asp\?id=\d+", restrict_xpaths=("//tr//b//a")),callback="parse_items",follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//span[contains(text(),'下一页')]/..")), follow=True),
    )

    def parse_items(self, response):
        item = DianQiZiDongHuaWangItem()
        pattern = re.compile(r'<title>(.*?)|.*?</title>',re.S)
        pattern_c = re.compile(r'<font color="#000066">(.*?)-中国电气自动化网\s*版权所有</font>',re.S)
        pattern_k = re.compile(r'<b>主营产品或服务：</b>(.*?) </td>',re.S)
        pattern_q = re.compile(r'(\d+)@qq.com',re.S)
        item["company_Name"] = response.xpath("//td[@class='bigfont']/text()").extract_first()
        item["company_address"] = response.xpath("///td[contains(text(),'地址：')]/following-sibling::td/text()").extract_first()
        item["linkman"] = response.xpath("//td[contains(text(),'联系：')]/following-sibling::td/text()").extract_first()
        item["telephone"] = response.xpath("//td[contains(text(),'电话：')]/following-sibling::td/text()").extract_first()
        item["phone"] = response.xpath("//td[contains(text(),'手机：')]/following-sibling::td/text()").extract_first()
        item["contact_Fax"] = response.xpath("//td[contains(text(),'传真：')]/following-sibling::td/font/text()").extract_first()
        item["contact_QQ"] = "".join(re.findall(pattern_q,response.text)) if re.findall(pattern_q,response.text) else ''
        item["E_Mail"] = response.xpath("//td[contains(text(),'电邮：')]/following-sibling::td/text()").extract_first()
        item["Source"] = response.url
        item["kind"] = "".join(re.findall(pattern_k,response.text)) if re.findall(pattern_k,response.text) else ''
        city_infos = response.xpath("//td[contains(text(),'区域：')]/following-sibling::td/text()").get()


        if item["company_Name"]:
            item["company_Name"] = self.cw.search_company(item["company_Name"])
        else:
            item["company_Name"] = ''
            return
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            # '工业平板电脑&nbsp;&nbsp;&nbsp;工业电脑&nbsp;&nbsp;工业一体机&nbsp;&nbsp;工控一体机&nbsp;'
            item["kind"] = item["kind"].replace(" ", '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '')\
                .replace('&nbsp','').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = self.cw.search_linkman(item["linkman"])
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
            item["company_address"] = item["company_address"].replace("联系地址：","")
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''

        if city_infos:
            if '.' in city_infos:
                try:
                    item["province"] = city_infos.split('.')[0]
                    item["city_name"] = city_infos.split('.')[1]
                except:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''
        else:
            item["province"] = ''
            item["city_name"] = ''

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''

    # def requests_href(self, url, headers):
    #     res = requests.get(url=url, headers=headers, timeout=10, verify=False)
    #     res.encoding = "utf-8"
    #     if res.status_code == requests.codes.ok:
    #         img = res.content
    #         something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img3\image.png"
    #         with open(something_img_file_path, "wb") as fp:
    #             fp.write(img)
    #         fp.close()
    #         if img:
    #             try:
    #                 something = recognition_image(something_img_file_path)
    #                 if something:
    #                     return something
    #                 else:
    #                     return ''
    #             except:
    #                 return ''
    #         else:
    #             return ''
    #     else:
    #         return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "eachina"])