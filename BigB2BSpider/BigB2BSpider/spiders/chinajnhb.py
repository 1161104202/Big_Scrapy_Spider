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
from BigB2BSpider.items import LvSeJieNengHuanBaoWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class LvSeJieNengHuanBaoWangSpider(CrawlSpider):
    name = "chinajnhb"
    allowed_domains = ['www.chinajnhb.com','chinajnhb.com']
    start_urls = ['http://www.chinajnhb.com/company-list/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.8,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "__cfduid=d4e12ed7152929d637dd24d6caa8595f61567821936; __yjsv3_shitong=1.0_7_5cc7bc17815e478fcd7be5681b440c5cbc6c_300_1567821937132_113.109.43.48_a159483a; cf_clearance=8a75e648bac7d28facb31e0697ee5d61f649f01a-1567821939-86400-150; Hm_lvt_9f3a77491e9245c6e630d675a97d358e=1567821944; Hm_lpvt_9f3a77491e9245c6e630d675a97d358e=1567824049",
            # "Host": "www.chinajnhb.com",
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
            allow=r".*",restrict_xpaths=("//div[@class='product_list']//div[@class='trade_info_name']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='pages']//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//a[contains(text(),'联系方式')]")), callback='parse_items', follow=True),

    )

    def parse_items(self, response):
        item = LvSeJieNengHuanBaoWangItem()
        pattern = re.compile(r'<meta name="keywords" content=".*?,(.*?)"/>',re.S)
        item["company_Name"] = response.xpath("//li[contains(text(),'·公司名称：')]/text()").extract_first()
        item["company_address"] = response.xpath("//li[contains(text(),'·公司地址：')]/text()").extract_first()
        item["linkman"] = response.xpath("//li[contains(text(),'·联系人：')]/text()").extract_first()
        item["telephone"] = response.xpath("//li[contains(text(),'·联系电话：')]/text()").extract_first()
        item["phone"] = response.xpath("//li[contains(text(),'·联系手机：')]/text()").extract_first()
        item["contact_Fax"] = response.xpath("//li[contains(text(),'·公司传真：')]/text()").extract_first()
        item["contact_QQ"] = response.xpath("//li[contains(text(),'·QQ号：')]/text()").extract_first()
        item["E_Mail"] = "".join(response.xpath("//li[contains(text(),'·电子邮件：')]//text()").extract())
        item["Source"] = response.url
        item["kind"] = ",".join(response.xpath("//p[contains(text(),'主营：')]//text()").getall())
        # city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()


        if item["company_Name"] and item["company_Name"] != '':
            item["company_Name"] = item["company_Name"].replace('·','')
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
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"].replace('未填写','').replace('·','')
        else:
            item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = item["phone"].replace('·','')
        else:
            item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = item["telephone"].replace('·','')
        else:
            item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = item["contact_Fax"].replace('·','')
        else:
            try:
                item["contact_Fax"] = item["telephone"]
            except:
                item["telephone"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        if item["E_Mail"]:
            item["E_Mail"] = item["E_Mail"].replace('·','')
        else:
            item["E_Mail"] = ''
        item["E_Mail"] = self.cw.search_email(item["E_Mail"])

        if item["contact_QQ"]:
            item["contact_QQ"] = item["contact_QQ"].replace('·','')
        else:
            item["contact_QQ"] = ''
        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

        if item["company_address"]:
            item["company_address"] = item["company_address"].replace('·','')
        else:
            item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        if item["company_address"]:
            pattern_p = re.compile(r'(.*?)省', re.S)
            pattern_c = re.compile(r'[省](.*?)[市镇县乡区]', re.S)
            try:
                item["province"] = "".join(re.findall(pattern_p, item["company_address"])) \
                    if re.findall(pattern_p, item["company_address"]) else ''
            except:
                item["province"] = ''
            try:
                item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                    if re.findall(pattern_p, item["company_address"]) else ''
            except:
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
    execute(["scrapy", "crawl", "chinajnhb"])