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
from BigB2BSpider.items import YiBiaoZhangLanWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class YiBiaoZhangLanWangSpider(CrawlSpider):
    name = "show18"
    allowed_domains = ['www.18show.cn','18show.cn']
    start_urls = ['http://www.18show.cn/product/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
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

    def parse(self, response):
        a_list = response.xpath("//div[@id='content']//div[@class='main-border']//div[@data-yz-king='true']//a")
        for a in a_list:
            kind_name = a.xpath("./@title").get()
            kind_href = a.xpath("./@href").get()
            if kind_href:
                kind_href = "http://www.18show.cn" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        a_list = response.xpath("//div[@class='productlist']//div[@class='info']//div[@class='info3']//div[@class='contactph']//a[@title='联系方式']")
        for a in a_list:
            contact_href = a.xpath("./@href").get()
            if contact_href and "/Contact.html" in contact_href:
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    # dont_filter=True
                )
        next_page_url = response.xpath("//a[@title='下一页']/@href").get()
        if next_page_url:
            next_page_url = "http://www.18show.cn" + (next_page_url.replace(' ','').strip())
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        if "网站暂时无法访问，造成不便，请谅解。" in response.text:
            return
        item = YiBiaoZhangLanWangItem()
        # ',,,联系人：,树伟,电话：,025-57467888,手机：,15806100000,更多联系方式>>,,,'
        pattern_c = re.compile(r'<title>联系我们 - (.*?)</title>',re.S)
        pattern_l = re.compile(r'>\s*联系人：(.*?)\s*<',re.S)
        pattern_tp = re.compile(r'>\s*联系电话：(.*?)\s*<', re.S)
        pattern_p = re.compile(r'>\s*移动电话：(.*?)\s*<', re.S)
        pattern_f = re.compile(r'>\s*传真：(.*?)\s*<', re.S)
        # pattern_e = re.compile(r'>\s*传真：(.*?)\s*<', re.S)
        pattern_a = re.compile(r'>\s*地址：(.*?)\s*<', re.S)
        pattern_q = re.compile(r'>\s*QQ：<a target=_blank href=http\:\/\/wpa\.qq\.com\/msgrd\?Uin=.*?>(.*?)</a>\s*<', re.S)
        item["company_Name"] = "".join(re.findall(pattern_c,response.text)) if re.findall(pattern_c,response.text) else ''
        item["kind"] = ",".join(response.xpath("//div[@class='pscSubCon1']//dl[@class='repeatItem']//dt//a//text()").getall())
        item["linkman"] = "".join(re.findall(pattern_l,response.text)) if re.findall(pattern_l,response.text) else ''
        item["telephone"] = "".join(re.findall(pattern_tp,response.text)) if re.findall(pattern_tp,response.text) else ''
        item["phone"] = "".join(re.findall(pattern_p,response.text)) if re.findall(pattern_p,response.text) else ''
        item["contact_Fax"] = "".join(re.findall(pattern_f,response.text)) if re.findall(pattern_f,response.text) else ''
        item["company_address"] = "".join(re.findall(pattern_a,response.text)) if re.findall(pattern_a,response.text) else ''
        item["contact_QQ"] = "".join(re.findall(pattern_q,response.text)) if re.findall(pattern_q,response.text) else ''
        item["E_Mail"] = response.xpath("//span[contains(text(),'电子邮件：')]/following-sibling::span/text()").get()
        item["Source"] = response.url
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
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"]
        else:
            try:
                item["linkman"] = "".join(response.xpath("//span[contains(text(),'联系人：')]//text()").getall())
            except:
                item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            try:
                item["phone"] = "".join(response.xpath("//span[contains(text(),'移动电话：')]//text()").getall())
                if not item["phone"]:
                    try:
                        item["phone"] = self.cw.search_phone_num(response.text)
                    except:
                        item["phone"] = ''
            except:
                item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            try:
                item["telephone"] = "".join(response.xpath("//span[contains(text(),'联系电话：')]//text()").getall())
                if item["telephone"]:
                    item["telephone"] = item["telephone"]
                else:
                    pattern_tp1 = re.compile(r'>电话：(.*?)<',re.S)
                    try:
                        item["telephone"] = "".join(re.findall(pattern_tp1,response.text)) \
                            if re.findall(pattern_tp1,response.text) else ''
                    except:
                        item["telephone"] = ''
            except:
                item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
        else:
            try:
                item["contact_Fax"] = "".join(response.xpath("//span[contains(text(),'传真号码：')]//text()").getall())
            except:
                item["contact_Fax"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        if item["E_Mail"]:
            item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        else:
            try:
                pattern_e = re.compile(r'>Email：(.*?)<',re.S)
                item["E_Mail"] = "".join(re.findall(pattern_e,response.text)) if re.findall(pattern_e,response.text) else ''
            except:
                item["E_Mail"] = ''
        item["E_Mail"] = self.cw.search_email(item["E_Mail"])

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
        else:
            try:
                item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
            except:
                item["contact_QQ"] = ''
        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

        if item["company_address"]:
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            try:
                item["company_address"] = "".join(response.xpath("//span[contains(text(),'公司地址：')]/..//text()").getall())
            except:
                item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

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
    execute(["scrapy", "crawl", "show18"])