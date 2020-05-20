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
from BigB2BSpider.items import LvDaoWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class LvDaoWangSpider(CrawlSpider):
    name = "alu"
    allowed_domains = ['www.alu.cn','alu.cn']
    start_urls = ['https://www.alu.cn/aluEnterprise/']
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
            allow=r".*",restrict_xpaths=("//div[@class='box990']//ul//li//div[@class='info']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='page']//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=(
                "//div[@class='wrap']//ul//a[contains(text(),'联系我们')]")), callback='parse_items', follow=True),

    )

    def parse_items(self, response):
        item = LvDaoWangItem()
        pattern = re.compile(r'<em>主营产品：</em>(.*?)\S*</p>',re.S)
        pattern1 = re.compile(r'</h3>\s*<strong>(.*?)</strong>\s*<p>',re.S)
        pattern2 = re.compile(r'<p><em>地址：</em>(.*?)<br />', re.S)
        pattern3 = re.compile(r'<em>电话：</em>(.*?)<br />', re.S)
        pattern4 = re.compile(r'<em>手机：</em>(.*?)<br />',re.S)
        pattern5 = re.compile(r'<em>传真：</em>(.*?)<br />', re.S)
        pattern6 = re.compile(r'<em>Email：</em>(.*?)<br />', re.S)
        pattern7 = re.compile(r'<em>QQ：</em>(.*?)<br />', re.S)
        pattern8 = re.compile(r'<li>所在地区：(.*?)</li>',re.S)
        pattern9 = re.compile(r'>主营：(.*?)<',re.S)
        item["company_Name"] = response.xpath("//div[@class='header']//div[@class='com']/h1/text()").extract_first()
        item["company_address"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
        item["linkman"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
        item["telephone"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
        item["phone"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
        item["contact_Fax"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
        item["contact_QQ"] = "".join(re.findall(pattern7,response.text)) if re.findall(pattern7,response.text) else ''
        item["E_Mail"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
        item["Source"] = response.url
        item["kind"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
        city_infos = ",".join(re.findall(pattern8,response.text)) if re.findall(pattern8,response.text) else ''


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
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            try:
                item["kind"] = "".join(re.findall(pattern9,response.text)[0]) if re.findall(pattern9,response.text) else ''
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            except:
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
            try:
                item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
            except:
                item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''

        if city_infos:
            # '广东 东莞'
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
    execute(["scrapy", "crawl", "alu"])