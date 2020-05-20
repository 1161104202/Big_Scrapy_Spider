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
from BigB2BSpider.items import ZhongGuoJiChuangWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ZhongGuoJiChuangWangSpider(CrawlSpider):
    name = "machine35"
    allowed_domains = ['www.machine35.com','achine35.com','search.machine35.com','vip.machine35.com']
    start_urls = ['http://www.machine35.com/company/']
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
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='content']//dl//dd//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*",
            restrict_xpaths=("//a[contains(text(),'联系方式')]")),callback="parse_items",follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//a[contains(text(),'下一页')]")), follow=True),
    )

    def parse_items(self, response):
        item = ZhongGuoJiChuangWangItem()
        pattern = re.compile(r"href='http:\/\/wpa.qq.com\/msgrd\?v=3&uin=(\d+)&site=machine35.com&menu=yes'",re.S)
        item["company_Name"] = "".join(response.xpath("//dt[@class='maintitle']//text()").extract())
        item["kind"] = response.xpath("//dd[@class='subtitle']/text()").get()
        item["company_address"] = response.xpath("//td[contains(text(),'地　　址：')]/following-sibling::td/text()").extract_first()
        item["linkman"] = response.xpath("///span[@class='blue']/text()").extract_first()
        item["telephone"] = response.xpath("//td[contains(text(),'电　　话：')]/following-sibling::td/text()").extract_first()
        item["phone"] = response.xpath("//td[contains(text(),'手　　机：')]/following-sibling::td/text()").extract_first()
        item["contact_Fax"] = response.xpath("///td[contains(text(),'传　　真：')]/following-sibling::td/text()").extract_first()
        item["contact_QQ"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
        item["E_Mail"] = response.xpath("//td[contains(text(),'邮　　箱：')]/following-sibling::td/text()").extract_first()
        item["Source"] = response.url
        city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()


        if item["company_Name"]:
            item["company_Name"] = self.cw.search_company(item["company_Name"])
        else:
            item["company_Name"] = ''
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(" ", '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：|供应商', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
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

        # if city_infos:
        if item["company_address"]:
            if '市' and '省' in item["company_address"]:
                try:
                    pattern_p = re.compile(r'(.*?)省', re.S)
                    pattern_c = re.compile(r'省(.*?)市', re.S)
                    item["province"] = "".join(re.findall(pattern_p, item["company_address"])) \
                        if re.findall(pattern_p, item["company_address"]) else ''
                    item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                        if re.findall(pattern_c, item["company_address"]) else ''
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
    execute(["scrapy", "crawl", "machine35"])