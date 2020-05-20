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
from BigB2BSpider.items import WuBaShiPingWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class WuBaShiPingWangSpider(CrawlSpider):
    name = "58food"
    allowed_domains = ['www.58food.com','58food.com']
    start_urls = ['http://www.58food.com/company/']
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
            allow=r".*",restrict_xpaths=("//div[@class='information-title']//dl//dt//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[@class='company-page-list']//div[@class='btn']//a[contains(text(),'查看联系方式')]")),callback='parse_items',follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='pages_m']//a[contains(text(),'下一页>>')]")), follow=True),
    )

    def parse_items(self, response):
        item = WuBaShiPingWangItem()
        # flag_pattern = re.compile(r'<div class="ictop"><strong>(.*?).CONTACT</strong><span>')
        # contact = re.findall(flag_pattern,response.text)
        if "联系方式.CONTACT" in response.text:
            item["company_Name"] = response.xpath("//div[@class='chname']/text()").extract_first()
            # item["company_id"] = self.get_md5(item["company_Name"])
            item["kind"] = response.xpath("//li[contains(text(),'主　　营：')]/text()").get()
            item["Source"] = response.url
            item["linkman"]= ''
            item["company_address"] = ''
            item["telephone"] = ''
            item["phone"] = ''
            item["contact_Fax"] = ''
            item["contact_QQ"] = ''
            item["E_Mail"] = ''
            item["province"] = ''
            item["city_name"] = ''

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
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：|主　　营：', '', item["kind"]).replace('-', '|')\
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
            else:
                item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))
            yield item

        else:
            pattern = re.compile(r'<meta name="keywords" content=".*?,(.*?)"/>',re.S)
            pattern_l = re.compile(r'<span>联&nbsp; 系&nbsp; 人：</span>(.*?)<br />',re.S)
            pattern_add = re.compile(r'<span>地　　址：</span>(.*?) .*?<br />',re.S)
            pattern_tp = re.compile(r'<span>联系电话：</span><i>(.*?)</i><br />',re.S)
            pattern_ph = re.compile(r'<span>联系手机：</span><i>(.*?)</i><br />',re.S)
            pattern_fx = re.compile(r'>\s*传　　真：(.*?)<br />',re.S)
            pattern_em = re.compile(r'>\s*邮　　箱：(.*?)<br />', re.S)
            pattern_qq = re.compile(r'(\d+)@qq.com',re.S)
            pattern_area  = re.compile(r'>\s*所在地区：(.*?)/(.*?)\s*<',re.S)
            item["company_Name"] = response.xpath("//div[@class='comname']/strong/text()").extract_first()
            item["company_address"] = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
            item["linkman"] = "".join(re.findall(pattern_l,response.text)) if re.findall(pattern_l,response.text) else ''
            item["telephone"] = "".join(re.findall(pattern_tp,response.text)) if re.findall(pattern_tp,response.text) else ''
            item["phone"] = "".join(re.findall(pattern_ph,response.text)) if re.findall(pattern_ph,response.text) else ''
            item["contact_Fax"] = "".join(re.findall(pattern_fx,response.text)) if re.findall(pattern_fx,response.text) else ''
            item["contact_QQ"] = "".join(re.findall(pattern_qq,response.text)) if re.findall(pattern_qq,response.text) else ''
            item["E_Mail"] = "".join(re.findall(pattern_em,response.text)) if re.findall(pattern_em,response.text) else ''
            item["Source"] = response.url
            item["kind"] = ",".join(response.xpath("//div[@class='comname']//span/text()").getall())
            # city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()
            item["province"] = "".join(re.findall(pattern_area,response.text)[0][0]) if re.findall(pattern_area,response.text) else ''
            item["city_name"] = "".join(re.findall(pattern_area,response.text)[0][1]) if re.findall(pattern_area,response.text) else ''


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

            if item["province"]:
                if " " in item["province"]:
                    try:
                        item["province"] = item["province"] = item["province"].split(' ')[0]
                    except:
                        item["province"] = ''
                elif "<" in item["province"]:
                    item["province"] = re.sub(r'\s|\r|t\n','',item["province"].split('<')[0])
            else:
                item["province"] = ''
            if item["city_name"]:
                if "css" in item["city_name"]:
                    item["city_name"] = ''
                else:
                    try:
                        item["city_name"] = re.sub(r'\s|\r|t\n','',item["city_name"].split(' ')[0])
                    except:
                        item["city_name"] = ''
            else:
                item["city_name"] = ''


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
    execute(["scrapy", "crawl", "58food"])