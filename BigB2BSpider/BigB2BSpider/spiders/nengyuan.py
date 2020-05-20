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
from BigB2BSpider.items import XinNengYuanWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class XinNengYuanWangSpider(CrawlSpider):
    name = "nengyuan"
    allowed_domains = ['www.china-nengyuan.com','china-nengyuan.com']
    start_urls = ['http://www.china-nengyuan.com/company/']
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
            allow=r".*",restrict_xpaths=("//table[6]//table[@class='cny_orange']//td//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//a[contains(text(),'更多联系方式>>')]")), callback='parse_items', follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//table[4]//table[6]//a[contains(text(),'下一页')]")), follow=True),

        # Rule(LinkExtractor(
        #     allow=r".*",restrict_xpaths=(
        #         "//div[@class='menu']//span[contains(text(),'联系方式')]/..")),  follow=True),

    )

    def parse_items(self, response):
        item = XinNengYuanWangItem()
        pattern = re.compile(r'(\d+)@qq.com',re.S)
        item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        item["company_address"] = response.xpath("//td[contains(text(),'详细地址：')]/following-sibling::td/text()").extract_first()
        item["linkman"] = response.xpath("//td[contains(text(),'　联系人：')]/following-sibling::td/text()").extract_first()
        item["telephone"] = response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/text()").extract_first()
        item["phone"] = response.xpath("//td[contains(text(),'　　手机：')]/following-sibling::td/text()").extract_first()
        item["contact_Fax"] = response.xpath("///td[contains(text(),'　　传真：')]/following-sibling::td/text()").extract_first()
        item["contact_QQ"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
        item["E_Mail"] = response.xpath("//td[contains(text(),'　　邮箱：')]/following-sibling::td/text()").extract_first()
        item["Source"] = response.url
        item["kind"] = response.xpath("//p[contains(text(),'主营产品：')]/text()").get()
        city_infos = response.xpath("//td[contains(text(),'所在城市：')]/following-sibling::td/text()").get()

        pattern_c = re.compile(r'<meta name="Keywords" content="(.*?),.*?" />',re.S)
        pattern_k = re.compile(r'<p>主营产品：(.*?)<br />',re.S)
        pattern_l = re.compile(r'>\s*联系人：(.*?)<br />',re.S)
        pattern_add = re.compile(r'>\s*通信地址：(.*?)&nbsp;',re.S)
        pattern_th = re.compile(r'>\s*公司电话：(.*?)<br />',re.S)
        pattern_ph = re.compile(r'>\s*手机：(.*?)<br />',re.S)
        pattern_fx = re.compile(r'>\s*传真：(.*?)<br />', re.S)
        pattern_em = re.compile(r'>\s*电子邮件：(.*?)<br />', re.S)


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
            try:
                item["company_Name"] = "".join(re.findall(pattern_c,response.text)) if re.findall(pattern_c,response.text) else ''
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            except:
                return
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(" ", '|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            try:
                item["kind"] = "".join(re.findall(pattern_k,response.text)) if re.findall(pattern_k,response.text) else ''
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            except:
                item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"].replace('未填写','')
        else:
            try:
                item["linkman"] = "".join(re.findall(pattern_l,response.text)) if re.findall(pattern_l,response.text) else ''
            except:
                item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            try:
                item["phone"] = "".join(re.findall(pattern_ph,response.text)) if re.findall(pattern_ph,response.text) else ''
            except:
                item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            try:
                item["telephone"] = "".join(re.findall(pattern_th,response.text)) if re.findall(pattern_th,response.text) else ''
            except:
                item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
        else:
            try:
                item["contact_Fax"] = "".join(re.findall(pattern_fx,response.text)) if re.findall(pattern_fx,response.text) else ''
            except:
                item["contact_Fax"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        if item["E_Mail"]:
            item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        else:
            try:
                item["E_Mail"] = "".join(re.findall(pattern_em,response.text)) if re.findall(pattern_em,response.text) else ''
            except:
                item["E_Mail"] = ''
        item["E_Mail"] = self.cw.search_email(item["E_Mail"])

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
        else:
            item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            try:
                item["company_address"] = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
            except:
                item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        if city_infos:
            if '/' in city_infos:
                try:
                    item["province"] = city_infos.split('/')[0]
                    item["city_name"] = city_infos.split('/')[1]
                except:
                    item["province"] = ''
                    item["city_name"] = ''
            elif ' ' in city_infos:
                try:
                    item["province"] = city_infos.split(' ')[0]
                    item["city_name"] = city_infos.split(' ')[1]
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
    execute(["scrapy", "crawl", "nengyuan"])