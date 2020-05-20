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
from BigB2BSpider.items import NongYeWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class NongYeWangSpider(CrawlSpider):
    name = "agronet"
    allowed_domains = ['www.agronet.com.cn','agronet.com.cn']
    start_urls = ['http://www.agronet.com.cn/Company']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "__cfduid=de2e2a6bb6c79f79ee0e4ca11eba9b53c1568193649; agronetCookie=D98233C159EF3AEA333D883B971C1FCA9B6F08A7476FD809; bdshare_firstime=1568193656351; __utmc=63149887; __utmz=63149887.1568193657.1.1.utmcsr=diqiuw.com|utmccn=(referral)|utmcmd=referral|utmcct=/b2bwangzhandaquan/nonglinmuyu/50753.html; Hm_lvt_8f396c620ee16c3d331cf84fd54feafe=1568193657; __yjsv3_shitong=1.0_7_5cc7bc17815e478fcd7be5681b440c5cbc6c_300_1568250975487_113.109.40.82_63352646; cf_clearance=1fdfdfe878d685b9a640cb2024384a132167861a-1568250977-31536000-150; Hm_lpvt_8f396c620ee16c3d331cf84fd54feafe=1568250980; __utma=63149887.12717690.1568193657.1568193657.1568250980.2; __utmt=1; __utmb=63149887.1.10.1568250980",
            "Host": "www.agronet.com.cn",
            "Pragma": "no-cache",
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
            allow=r".*",restrict_xpaths=("//dd[@class='area_lists']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[@class='main']//ul//li//em//a[contains(text(),'联系方式')]")),callback="parse_items",follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//a[contains(text(),'下一页')]")), follow=True),
    )


    def parse_items(self, response):
        item = NongYeWangItem()
        pattern_c = re.compile(r'<meta name="keywords" content="(.*?)" />',re.S)
        pattern_k = re.compile(r'>主营：(.*?)\s*<',re.S)
        pattern_area = re.compile(r'>\s*公司所在地：(.*?)  (.*?)  <br/>',re.S)
        # pattern_add = re.compile(r'>\s*地址：(.*?)<br />',re.S)
        # pattern_tp = re.compile(r'>\s*电话：(.*?)<br />',re.S)
        # pattern_ph = re.compile(r'>\s*手机：(.*?)<br />',re.S)
        # pattern_fx = re.compile(r'>\s*传真：(.*?)<br />',re.S)
        pattern_ad = re.compile(r'>\s*地址：(.*?)<',re.S)
        pattern_add = re.compile(r'址：(.*?)<', re.S)
        pattern_tp = re.compile(r'话：(.*?)<', re.S)
        pattern_ph = re.compile(r'机：(.*?)<', re.S)
        pattern_fx = re.compile(r'真：(.*?)<', re.S)
        pattern_e = re.compile(r'箱：(.*?)<')


        pattern_em = re.compile(r'>\s*邮箱：<a href=".*?">(.*?)</a><br />',re.S)
        pattern_qq = re.compile(r'(\d+)@qq.com',re.S)
        item["company_Name"] = "".join(re.findall(pattern_c,response.text)) if re.findall(pattern_c,response.text) else ''
        item["company_address"] = "".join(re.findall(pattern_ad,response.text)) if re.findall(pattern_ad,response.text) else ''
        item["linkman"] = "".join(response.xpath("//li[contains(text(),'联系人：')]/text()").extract())
        item["telephone"] = "".join(re.findall(pattern_tp,response.text)) if re.findall(pattern_tp,response.text) else ''
        item["phone"] = "".join(re.findall(pattern_ph,response.text)) if re.findall(pattern_ph,response.text) else ''
        item["contact_Fax"] = "".join(re.findall(pattern_fx,response.text)) if re.findall(pattern_fx,response.text) else ''
        item["contact_QQ"] = "".join(re.findall(pattern_qq,response.text)) if re.findall(pattern_qq,response.text) else ''
        item["E_Mail"] = "".join(re.findall(pattern_em,response.text)) if re.findall(pattern_em,response.text) else ''
        item["Source"] = response.url
        item["kind"] = ",".join(response.xpath("//p[contains(text(),'主营：')]//text()").getall()) or "".join(response.xpath("//div[@class='main_product_info']//text()").getall())
        # city_infos = response.xpath("//td[contains(text(),'所在地区：')]/following-sibling::td/text()").get()
        item["province"] = "".join(re.findall(pattern_area, response.text)[0][0]) if re.findall(pattern_area,response.text) else ''
        item["city_name"] = "".join(re.findall(pattern_area, response.text)[0][1]) if re.findall(pattern_area,response.text) else ''


        if item["company_Name"]:
            item["company_Name"] = self.cw.search_company(item["company_Name"])
        else:
            item["company_Name"] = ''
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"] and item["kind"] != '':
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
            item["linkman"] = self.cw.search_linkman(item["linkman"])
        else:
            try:
                item["linkman"] = "".join(response.xpath("//p[@class='fd_zw']//b//text()").getall())
                item["linkman"] = re.sub(r'\s|\r|\t|\n','',item["linkman"])
            except:
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
            try:
                item["E_Mail"] = "".join(re.findall(pattern_e,response.text)) if re.findall(pattern_e,response.text) else ''
            except:
                item["E_Mail"] = ''
        item["E_Mail"] = self.cw.search_email(item["E_Mail"])

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
        else:
            item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = item["company_address"].replace("联系地址：","")
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            try:
                item["company_address"] = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
            except:
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
    execute(["scrapy", "crawl", "agronet"])