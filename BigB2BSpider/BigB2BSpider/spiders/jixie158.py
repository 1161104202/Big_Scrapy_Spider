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
from BigB2BSpider.items import YiWuBaJiXieWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class YiWuBaJiXieWangSpider(CrawlSpider):
    name = "jixie158"
    allowed_domains = ['www.158jixie.com','158jixie.com']
    start_urls = ['http://www.158jixie.com/ability/']
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
            allow=r"\/company\/.*?\/",restrict_xpaths=("//div[@class='cell1_22_2']//tr//td//a")),follow=True),

        Rule(LinkExtractor(
            allow=r"\/company/\d+\/", restrict_xpaths=("//div[@id='page3_mid1_2']//div[@class='cell1_2']//tr//td//p//a")),callback="parse_items",follow=True),

        Rule(LinkExtractor(
            allow=r"index.aspx\?myID=\d+\&Pindex=\d+", restrict_xpaths=("//span[@id='com_rep1_1_pageNumLab']//a")), follow=True),
    )

    def parse_items(self, response):
        item = YiWuBaJiXieWangItem()
        pattern = re.compile(r'<title>(.*?)</title>',re.S)
        pattern_kd = re.compile(r'<p>.*? - 主营产品：(.*?) </p>', re.S)
        pattern_c = re.compile(r'<span>公司名称：</span>(.*?)<br>', re.S)
        pattern_tp = re.compile(r'<b>联系电话：</b>(.*?)<br/>', re.S)
        pattern_ph = re.compile(r'<b>联系手机：</b>(.*?)<br/>', re.S)
        pattern_fx = re.compile(r'<b>联系传真：</b>(.*?)<br/>', re.S)
        pattern_lm = re.compile(r'<b>联系人：</b>(.*?)<br/>', re.S)
        pattern_em = re.compile(r'<b>联系邮件：</b>(.*?)<br/>',re.S)
        pattern_add = re.compile(r'<b>联系地址：</b>(.*?)<br/>', re.S)
        pattern_area = re.compile(r'<span>所在省份：</span>(.*?)<br>', re.S)
        pattern_qq = re.compile(r'(\d+)@qq.com', re.S)

        item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
        item["company_address"] = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
        item["linkman"] = "".join(re.findall(pattern_lm,response.text)) if re.findall(pattern_lm,response.text) else ''
        item["telephone"] = "".join(re.findall(pattern_tp,response.text)) if re.findall(pattern_tp,response.text) else ''
        item["phone"] = "".join(re.findall(pattern_ph,response.text)) if re.findall(pattern_ph,response.text) else ''
        item["contact_Fax"] = "".join(re.findall(pattern_fx,response.text)) if re.findall(pattern_fx,response.text) else ''
        item["contact_QQ"] = "".join(re.findall(pattern_qq,response.text)) if re.findall(pattern_qq,response.text) else ''
        item["E_Mail"] = "".join(re.findall(pattern_em,response.text)) if re.findall(pattern_em,response.text) else ''
        item["Source"] = response.url
        item["kind"] = ",".join(response.xpath("//strong[contains(text(),'主营业务：')]/../text()").getall())
        city_infos = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''


        if item["company_Name"]:
            item["company_Name"] = self.cw.search_company(item["company_Name"])
        else:
            item["company_Name"] = ''
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
            item["linkman"] = self.cw.search_linkman(item["linkman"])
        else:
            item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            # if ' ' in item["phone"]:
            #     item["phone"] = item["phone"].replace(' ',',')
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
            if '市' and '省' in city_infos:
                try:
                    pattern_p = re.compile(r'(.*?)省', re.S)
                    pattern_c = re.compile(r'省(.*?)市', re.S)
                    item["province"] = "".join(re.findall(pattern_p, city_infos)) \
                        if re.findall(pattern_p, city_infos) else ''
                    item["city_name"] = "".join(re.findall(pattern_c, city_infos)) \
                        if re.findall(pattern_c, city_infos) else ''
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
    execute(["scrapy", "crawl", "jixie158"])