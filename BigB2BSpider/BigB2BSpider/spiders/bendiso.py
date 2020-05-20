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
from BigB2BSpider.items import BenDiSouWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class BenDiSouWangSpider(CrawlSpider):
    name = "bendiso"
    allowed_domains = ['www.bendiso.com','bendiso.com']
    start_urls = ['http://www.bendiso.com/gongsi/']
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

    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@id='main']//ul//li//div[@class='picture']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='page']//a[@title='下一页']")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='nav']//a[contains(text(),'联系方式')]")), callback='parse_items', follow=True),


    )

    def parse_items(self, response):
        item = BenDiSouWangItem()
        pattern = re.compile(r'<meta name="keywords" content=".*?,(.*?)"/>',re.S)
        item["company_Name"] = response.xpath("//div[@id='header']//h1//a/text()").extract_first()
        item["company_address"] = response.xpath("//div[@class='corp_boxinfo']//p[contains(text(),'地址：')]/text()").extract_first()
        item["linkman"] = response.xpath("//p[contains(text(),'联系人：')]/text()").extract_first()
        item["telephone"] = response.xpath("//p[contains(text(),'电话：')]/text()").extract_first()
        item["phone"] = response.xpath("//p[contains(text(),'手机：')]/text()").extract_first()
        item["contact_Fax"] = response.xpath("//p[contains(text(),'传真：')]/text()").extract_first()
        item["contact_QQ"] = response.xpath("//p[contains(text(),'QQ：')]//img[@alt='点击这里给我发消息']/../@href").extract_first()
        item["E_Mail"] = response.xpath("//p[contains(text(),'邮箱：')]/a/text()").extract_first()
        item["Source"] = response.url
        item["kind"] = ",".join(response.xpath("//ul[@class='product_boxli']//li//div[@class='info']//a/@title").getall())
        city_infos = response.xpath("//div[@class='corp_boxinfo']//p[contains(text(),'地址：')]/text()").get()


        if item["company_Name"] and item["company_Name"] != '':
            if "（" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('（')[0]
            elif "(" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('(')[0]
            elif "_" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('_')[0]
            elif "-" in item["company_Name"]:
                item["company_Name"] = item["company_Name"].split('-')[0]
            else:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        else:
            return
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(" ", '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：|', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"].replace('未填写','')
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

        if city_infos:
            if ' ' in city_infos:
                try:
                    city_infos = city_infos.replace("地址：", "")
                    item["province"] = city_infos.split(' ')[0]
                    item["city_name"] = city_infos.split(' ')[1]
                except:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''
        else:
            # pattern_p = re.compile(r'([\u4e00-\u9fa5]{2,5})省')
            # pattern_c = re.compile(r'[省]([\u4e00-\u9fa5]{2,5})市')

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
    execute(["scrapy", "crawl", "bendiso"])