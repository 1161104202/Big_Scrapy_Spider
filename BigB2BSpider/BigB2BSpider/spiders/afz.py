# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import AnFangZhanspiderItem
from scrapy.cmdline import execute



class AnFangZhanSpider(CrawlSpider):
    name = 'afz'
    allowed_domains = ['afzhan.com','www.afzhan.com']
    start_urls = ['http://www.afzhan.com/company/']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_081b84205c0f16480d7a8964a70f6b6b=1565055009; BAIDU_SSP_lcr=http://hao.huangye88.com/b2b_42621.html; Hm_lpvt_081b84205c0f16480d7a8964a70f6b6b=1565055034",
            # "Host": "www.fashangji.com",
            # "Referer": "https://www.fashangji.com/",
            # "Sec-Fetch-Mode": "navigate",
            # "Sec-Fetch-Site": "none",
            # "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='locality']//a")
        for a in a_list:
            # print(a)
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_name is None:
                kind_name = a.xpath("./strong/text()").extract_first()
            if kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        dt_list = response.xpath("//div[@class='companyList']//dt")
        for dt in dt_list:
            item = AnFangZhanspiderItem()
            item["company_Name"] = dt.xpath(".//div[@class='companyName']//a/@title").extract_first()
            company_href = dt.xpath(".//div[@class='companyName']//a/@href").extract_first()
            item["kind"] = dt.xpath(".//i[contains(text(),'主营产品')]/../text()").extract_first()
            # item["company_address"] = dt.xpath(".//div[@class='company2-c']//p[contains(text(),'公司地址：')]/text()").extract_first()
            # contact_infos = div.xpath(".//div[@class='company2-c']//p[contains(text(),'联系方式：')]/text()").extract_first()
            item["province"] = ''
            item["city_name"] = ''

            if company_href:
                # print(company_href)
                contact_href = "http://www.afzhan.com" + company_href + "/contactus.html"
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='page']//a[@title='下一页']/@href").extract_first()
        if next_page_url:
            next_page_url = "http://www.afzhan.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        item = response.meta["item"]
        pattern = re.compile(r'联系人：(.*?)<br />',re.S)
        pattern1 = re.compile(r'电话：(.*?)<br />', re.S)
        pattern2 = re.compile(r'传真：(.*?)<br />', re.S)
        pattern3 = re.compile(r'手机：(.*?)<br />', re.S)
        pattern4 = re.compile(r'地址：(.*?)<br />', re.S)
        pattern5 = re.compile(r'>(.*?)</label>',re.S)

        pattern6 = re.compile(r'<p>联 系 人  ：  <i>(.*?)</i>', re.S)
        pattern7 = re.compile(r'<p>电<b></b>话：    (.*?) </p>', re.S)
        pattern8 = re.compile(r'<p>传<b></b>真：    (.*?)</p>', re.S)
        pattern9 = re.compile(r'<p>手<b></b>机：    (.*?) </p>', re.S)
        pattern10 = re.compile(r'<p>详细地址：    (.*?) </p>', re.S)

        # item["company_Name"] = response.xpath("//div[@class='contenttext']/p/text()").extract_first()
        # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
        # item["kind"] = response.xpath("//div[@class='head']/h4/text()").extract_first()
        item["company_address"] = "".join(
            response.xpath("//dt[contains(text(),'地')]/following-sibling::dd/text()").extract())
        item["linkman"] = "".join(
            response.xpath("//strong[contains(text(),'联系人')]/text()").extract())
        item["telephone"] = "".join(
            response.xpath("//dt[contains(text(),'电')]/following-sibling::dd/text()").extract())
        item["phone"] = "".join(
            response.xpath("//dt[contains(text(),'手')]/following-sibling::dd/text()").extract())
        item["contact_Fax"] = "".join(
            response.xpath("//dt[contains(text(),'传')]/following-sibling::dd/text()").extract())
        item["contact_QQ"] = "".join(response.xpath("//a[@class='share']/@href").extract())
        item["E_Mail"] = ""
        item["Source"] = response.url

        city_infos = "".join(
            response.xpath("//td[contains(text(),'所在地区：')]/following-sibling::td/text()").extract())

        if city_infos:
            # 广东/潮州市
            try:
                item["province"] = city_infos.split("/")[0]
                item["city_name"] = city_infos.split("/")[1]
            except:
                item["province"] = city_infos
                item["city_name"] = ''
        else:
            item["province"] = ''
            item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|经营范围：', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace('，', '|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"]
        else:
            try:
                item["linkman"] = "".join(re.findall(pattern,response.text)) if response.text else ''
                if item["linkman"]:
                    pass
                else:
                    try:
                        item["linkman"] = "".join(re.findall(pattern6, response.text)) if response.text else ''
                    except:
                        item["linkman"] = ''
            except:
                item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = item["phone"]
        else:
            try:
                item["phone"] = "".join(re.findall(pattern3,response.text)) if response.text else ''
                if item["phone"]:
                    pass
                else:
                    try:
                        item["phone"] = "".join(re.findall(pattern9, response.text)) if response.text else ''
                    except:
                        item["phone"] = ''
            except:
                item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = item["telephone"]
        else:
            try:
                item["telephone"] = "".join(re.findall(pattern1, response.text)) if response.text else ''
                if item["telephone"]:
                    pass
                else:
                    try:
                        item["telephone"] = "".join(re.findall(pattern7, response.text)) if response.text else ''
                    except:
                        item["telephone"] = ''
            except:
                item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = item["contact_Fax"]
        else:
            try:
                item["contact_Fax"] = "".join(re.findall(pattern2, response.text)) if response.text else ''
                if item["contact_Fax"]:
                    pass
                else:
                    try:
                        item["contact_Fax"] = "".join(re.findall(pattern8, response.text)) if response.text else ''
                    except:
                        item["contact_Fax"] = ''
            except:
                item["contact_Fax"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        # if item["E_Mail"]:
        #     item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        #     item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
        # else:
        #     item["E_Mail"] = ''
        #     item["contact_QQ"] = ''

        if item["contact_QQ"]:
            item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
        else:
            item["contact_QQ"] = ''
        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

        if item["company_address"]:
            item["company_address"] = item["company_address"]
        else:
            try:
                item["company_address"] = "".join(re.findall(pattern4, response.text)) if response.text else ''
                if item["company_address"]:
                    pass
                else:
                    try:
                        item["company_address"] = "".join(re.findall(pattern10, response.text)) if response.text else ''
                    except:
                        item["company_address"] = ''
            except:
                item["company_address"] = ''
        if item["company_address"]:
            try:
                item["company_address"] = item["company_address"].split("</")[0]
            except:
                item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''

    # def requests_href(self, url, headers):
    #     res = requests.get(url=url, headers=headers, timeout=20, verify=False)
    #     res.encoding = "utf-8"
    #     if res.status_code == requests.codes.ok:
    #         img = res.content
    #         something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img\image.png"
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
    execute(["scrapy", "crawl", "afz"])