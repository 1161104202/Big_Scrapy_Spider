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
from BigB2BSpider.items import TongZhuangQiYeWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class LuYiYiFuWangSpider(CrawlSpider):
    name = "ef61"
    allowed_domains = ['corp.61ef.cn']
    start_urls = ['http://corp.61ef.cn/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            # "Connection": "keep-alive",
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
            allow=r".*",restrict_xpaths=("//dl[@id='OnAdrees']//dd//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//ul[@class='menber-list']//li//h3//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='page']//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='nav']//a[contains(text(),'联系我们')]")), callback="parse_items",
            follow=True),
    )


    def parse_items(self, response):
        item = TongZhuangQiYeWangItem()
        pattern_em = re.compile(r'(.*?)@163.com',re.S)
        pattern_qq = re.compile(r'(\d+)@qq.com',re.S)
        item["company_Name"] = "".join(response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td//text()").getall())
        item["company_address"] = "".join(response.xpath("//td[contains(text(),'地　　址：')]/following-sibling::td//text()").getall())
        item["linkman"] = "".join(response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td//text()").getall())
        item["telephone"] = response.xpath("//td[contains(text(),'电　　话：')]/following-sibling::td/a/@txt").get()
        item["phone"] = response.xpath("//td[contains(text(),'电　　话：')]/following-sibling::td/a/@txt").get()
        item["contact_Fax"] = response.xpath("//td[contains(text(),'电　　话：')]/following-sibling::td/a/@txt").get()
        item["contact_QQ"] = "".join(re.findall(pattern_qq,response.text)) if re.findall(pattern_qq,response.text) else ''
        item["E_Mail"] = "".join(re.findall(pattern_em,response.text)) if re.findall(pattern_em,response.text) else ''
        item["Source"] = response.url
        item["kind"] = "童装|服装"
        item["province"] = ""
        item["city_name"] = ""
        # city_infos = response.xpath("//td[contains(text(),'所在地区：')]/following-sibling::td/text()").get()
        # item["province"] = "".join(re.findall(pattern_area, response.text)[0][0]) if re.findall(pattern_area,response.text) else ''
        # item["city_name"] = "".join(re.findall(pattern_area, response.text)[0][1]) if re.findall(pattern_area,response.text) else ''


        if item["company_Name"]:
            item["company_Name"] = self.cw.search_company(item["company_Name"])
        else:
            item["company_Name"] = ''
            return
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"] and item["kind"] != '':
            item["kind"] = item["kind"].replace(" ", '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            # try:
            #     item["kind"] = "".join(re.findall(pattern_k,response.text)) if re.findall(pattern_k,response.text) else ''
            #     item["kind"] = item["kind"].replace(" ", '|')
            #     item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
            #         .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            # except:
                item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = self.cw.search_linkman(item["linkman"])
        else:
            # try:
            #     item["linkman"] = "".join(response.xpath("//p[@class='fd_zw']//b//text()").getall())
            #     item["linkman"] = re.sub(r'\s|\r|\t|\n','',item["linkman"])
            # except:
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
            # try:
            #     item["E_Mail"] = "".join(re.findall(pattern_e,response.text)) if re.findall(pattern_e,response.text) else ''
            # except:
                item["E_Mail"] = ''
        item["E_Mail"] = self.cw.search_email(item["E_Mail"])

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
        else:
            item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = item["company_address"]
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            # try:
            #     item["company_address"] = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
            # except:
                item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        # if city_infos:
        #     if '/' in city_infos:
        #         try:
        #             item["province"] = city_infos.split('/')[0]
        #             item["city_name"] = city_infos.split('/')[1]
        #         except:
        #             item["province"] = ''
        #             item["city_name"] = ''
        #     else:
        #         item["province"] = ''
        #         item["city_name"] = ''
        # else:
        #     item["province"] = ''
        #     item["city_name"] = ''

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
    execute(["scrapy", "crawl", "ef61"])