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
from BigB2BSpider.items import HuangQiuXieYeWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class HuangQiuXieYeWangSpider(CrawlSpider):
    name = "shoes"
    allowed_domains = ['www.shoes.net.cn','shoes.net.cn']
    start_urls = ['http://www.shoes.net.cn/company/']
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
            allow=r".*",restrict_xpaths=("//dl[contains(@class,'item')]//dt//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[@class='company_box']//div[@class='f_btn']//a[@class='line']")),callback='parse_items',follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='pag_pages']//a[contains(text(),'>')]")), follow=True),
    )

    def parse_items(self, response):
        item = HuangQiuXieYeWangItem()
        if "http://www.shoes.net.cn/company" in response.url:
            item["company_Name"] = response.xpath("//h2[@id='Header_hCompanyName']/text()").get()
            item["kind"] = ",".join(response.xpath("//dt[contains(text(),'主营产品')]/following-sibling::dd//a//text()").getall())
            item["company_address"] = response.xpath("//dt[contains(text(),'电话')]/following-sibling::dd[2]/text()").get()
            item["linkman"] = response.xpath("//dt[contains(text(),'联系人')]/following-sibling::dd[1]/text()").get()
            item["telephone"] = response.xpath("//dt[contains(text(),'电话')]/following-sibling::dd[1]/text()").get()
            item["phone"] = response.xpath("//dt[contains(text(),'手机')]/following-sibling::dd[1]/text()").get()
            item["contact_Fax"] = response.xpath("//dt[contains(text(),'传真')]/following-sibling::dd[1]/text()").get()
            item["contact_QQ"] = response.xpath("//dt[contains(text(),'Email')]/following-sibling::dd[1]/text()").get()
            item["E_Mail"] = response.xpath("//dt[contains(text(),'Email')]/following-sibling::dd[1]/text()").get()
            item["Source"] = response.url
            item["province"] = ''
            item["city_name"] = ''
            if item["company_Name"]:
                item["company_Name"] = self.cw.search_company(item["company_Name"])
                item["company_id"] = self.get_md5(item["company_Name"])
            else:
                return
            if item["kind"]:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            else:
                item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"].replace('--', '')
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
        else:
            pattern_c = re.compile(r'<h2><span>(.*?)</span></h2>', re.S)
            pattern_k = re.compile(r'<li><span>主营：</span>(.*?)</li>', re.S)
            pattern_area = re.compile(r' <li><span>所在地区：</span>(.*?)</li>', re.S)
            # pattern_add = re.compile(r'>\s*地址：(.*?)<br />',re.S)
            # pattern_tp = re.compile(r'>\s*电话：(.*?)<br />',re.S)
            # pattern_ph = re.compile(r'>\s*手机：(.*?)<br />',re.S)
            # pattern_fx = re.compile(r'>\s*传真：(.*?)<br />',re.S)
            pattern_ad = re.compile(r'>\s*地址：(.*?)<', re.S)
            pattern_add = re.compile(r'\s*地址：(.*?)<', re.S)
            pattern_tp = re.compile(r'>\s*电话：(.*?)<', re.S)
            pattern_ph = re.compile(r'>\s*手机：(.*?)<', re.S)
            pattern_fx = re.compile(r'>\s*传真：(.*?)<', re.S)
            pattern_e = re.compile(r'>\s*Email：(.*?)<', re.S)
            pattern_em = re.compile(r'>邮箱：(.*?)<', re.S)
            pattern_u = re.compile(r'站：(.*?)<', re.S)
            pattern_l = re.compile(r'>联系人：(.*?)<', re.S)
            pattern_qq = re.compile(r'(\d+)@qq.com', re.S)

            item["company_Name"] = "".join(re.findall(pattern_c, response.text)) if re.findall(pattern_c,
                                                                                               response.text) else ''
            item["company_address"] = "".join(re.findall(pattern_ad, response.text)) if re.findall(pattern_ad,
                                                                                                    response.text) else ''
            item["linkman"] = "".join(re.findall(pattern_l, response.text)) if re.findall(pattern_l,
                                                                                          response.text) else ''
            item["telephone"] = "".join(re.findall(pattern_tp, response.text)) if re.findall(pattern_tp,
                                                                                             response.text) else ''
            item["phone"] = "".join(re.findall(pattern_ph, response.text)) if re.findall(pattern_ph,
                                                                                         response.text) else ''
            item["contact_Fax"] = "".join(re.findall(pattern_fx, response.text)) if re.findall(pattern_fx,
                                                                                               response.text) else ''
            item["contact_QQ"] = "".join(re.findall(pattern_qq, response.text)) if re.findall(pattern_qq,
                                                                                              response.text) else ''
            item["E_Mail"] = "".join(re.findall(pattern_e, response.text)) if re.findall(pattern_e,
                                                                                         response.text) else ''
            item["Source"] = response.url
            item["kind"] = "".join(re.findall(pattern_k, response.text)) if re.findall(pattern_k, response.text) else ''
            item["province"] = ''
            item["city_name"] = ''
            # city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()

            if item["company_Name"] and item["company_Name"] != '':
                item["company_Name"] = self.cw.search_company(item["company_Name"])
            else:
                return

            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            else:
                item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"].replace('未填写', '')
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
    execute(["scrapy", "crawl", "shoes"])