# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import WangLuoYiYiSispiderItem
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class WangLuoYiYiSiSpider(RedisCrawlSpider):
    name = 'nt114'
    allowed_domains = ['net114.com','www.net114.com','corp.net114.com',
                       'acntian-yi_d.net114.com','ahzdt_d.net114.com',
                       'mmr_deng.net114.com','ad4a1v22i9d4_d.net114.com']
    cw = CleanWords()
    redis_key = "nt114:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_34c005d4caf30d75012a05867beca619=1562747829,1564973957;
            # Hm_lpvt_34c005d4caf30d75012a05867beca619=1564974049",
            # "Host": "b2b.huishangbao.com",
            # "Referer": "http://b2b.huishangbao.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        },

        # 不验证SSL证书
    #     "DOWNLOAD_HANDLERS_BASE" : {
    #     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    #     'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    #     'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    #     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
    # },
    # "DOWNLOAD_HANDLERS" : {
    #     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'}
    }

    def start_requests(self):
        start_urls = ['http://corp.net114.com/']
        start_urls = start_urls[0]
        yield scrapy.Request(
            url=start_urls,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        a_list = response.xpath("//div[@class='container']//div[@class='center-bg']"
                                "//div[contains(@class,'enterprise-box')]//ul//li//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_name is None:
                kind_name = a.xpath("./@title").extract_first()
            if kind_href and "search." not in kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        div_list = response.xpath("//div[@id='offer_data_list']//div[contains(@class,'enter-list')]")
        for div in div_list:
            item = WangLuoYiYiSispiderItem()
            pattern = re.compile(r'地       址：(.*?)省(.*?)市.*?', re.DOTALL)
            item["company_Name"] = "".join(div.xpath(".//div[@class='enter-title']"
                                                     "//a[@class='corp-title']//text()").extract())
            company_href = div.xpath(".//div[@class='enter-title']//a[@class='corp-title']/@href").extract_first()
            item["kind"] = "".join(div.xpath(".//p[contains(text(),'主营产品：')]/..//text()").extract())
            item["company_address"] = "".join(div.xpath(".//p[contains(text(),'址：')]/..//text()").extract())
            # '地       址：河北省大城县毕演马'
            city_infos = item["company_address"]
            if city_infos:
                # 广东/潮州市
                try:
                    item["province"] = re.findall(pattern, city_infos)[0][0]
                    item["city_name"] = re.findall(pattern, city_infos)[0][1]
                except:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''
            if company_href:
                # print(company_href)
                if "detail." in company_href:
                    contact_href = company_href
                else:
                    contact_href = company_href + "contactus.html"
                    # print(contact_href)
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@id='paging']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page_url:
            next_page_url = "http://corp.net114.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_contact(self, response):
        if "您查看的页面暂时不能访问哦！" in response.text:
            return
        pattern = re.compile(r'>公司名称：(.*?)<',re.S)
        pattern1 = re.compile(r'>联系人：(.*?)<', re.S)
        pattern2 = re.compile(r'>>联系电话：(.*?)<', re.S)
        pattern3 = re.compile(r'>传真：(.*?)<', re.S)
        pattern4 = re.compile(r'>手机：(.*?)<', re.S)
        pattern5 = re.compile(r'地址：(.*?)<', re.S)
        item = response.meta["item"]
        if response.text:
            if "contactus." in response.url:
                # item["company_Name"] = response.xpath("//p[contains(text(),'公司名称：')]/text()").extract_first()
                # item["company_address"] = "".join(response.xpath("//p[contains(text(),'地址：')]/text()").extract())
                item["linkman"] = "".join(response.xpath("//p[contains(text(),'联系人：')]/text()").extract())
                item["telephone"] = "".join(response.xpath("//p[contains(text(),'联系电话：')]/text()").extract())
                item["phone"] = "".join(response.xpath("//p[contains(text(),'手机：')]/text()").extract())
                item["E_Mail"] = response.xpath("//p[contains(text(),'电子邮件：')]/text()").extract_first()
                item["contact_Fax"] = response.xpath("//p[contains(text(),'传真：')]/text()").extract_first()
                item["contact_QQ"] = "".join(response.xpath("//img[@title='点击这里给我发消息']/../@href").extract())
                item["Source"] = response.url

                if item["company_Name"]:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|·公司名称：', '', item["company_Name"])\
                        .replace(' ', '').strip()
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营产品：', '', item["kind"])\
                        .replace('-', '|').replace('、', '|') \
                        .replace('，', '|').replace('，', '|').replace('.', '').strip()
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    if "（" in item["linkman"]:
                        item["linkman"] = item["linkman"].split("（")[0]
                    else:
                        item["linkman"] = item["linkman"]
                else:
                    try:
                        item["linkman"] = "".join(re.findall(pattern1,response.text)) \
                            if re.findall(pattern1,response.text) else ''
                    except:
                        item["linkman"] = ''
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if item["phone"]:
                    item["phone"] = item["phone"]
                else:
                    try:
                        item["phone"] = "".join(re.findall(pattern4,response.text)) \
                            if re.findall(pattern4,response.text) else ''
                    except:
                        item["phone"] = ''
                item["phone"] = self.cw.search_phone_num(item["phone"])

                if item["telephone"]:
                    item["telephone"] = item["telephone"]
                else:
                    try:
                        item["telephone"] = "".join(re.findall(pattern2,response.text)) \
                            if re.findall(pattern2,response.text) else ''
                    except:
                        item["telephone"] = ''
                item["telephone"] = self.cw.search_telephone_num(item["telephone"])

                if item["contact_Fax"]:
                    item["contact_Fax"] = item["contact_Fax"]
                else:
                    try:
                        item["contact_Fax"] = "".join(re.findall(pattern2,response.text)) \
                            if re.findall(pattern3,response.text) else ''
                    except:
                        item["contact_Fax"] = ''
                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

                if item["E_Mail"]:
                    item["E_Mail"] = self.cw.search_email(item["E_Mail"])
                else:
                    item["E_Mail"] = ''

                if item["contact_QQ"]:
                    item["contact_QQ"] = item["contact_QQ"]
                else:
                    item["contact_QQ"] = ''
                item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

                if item["company_address"]:
                    item["company_address"] = item["company_address"]
                else:
                    try:
                        item["company_address"] = "".join(re.findall(pattern5,response.text)) \
                            if re.findall(pattern5,response.text) else ''
                    except:
                        item["company_address"] = ''
                item["company_address"] = self.cw.search_address(item["company_address"])

                # if item["host_href"]:
                #     item["host_href"] = item["host_href"]
                # else:
                #     item["host_href"] = ''

                yield item

            else:
                # item["company_Name"] = response.xpath("//p[contains(text(),'公司名称：')]/text()").extract_first()
                # item["company_address"] = "".join(response.xpath("//span[contains(text(),'详细地址：')]/..//text()").extract())
                item["linkman"] = "".join(response.xpath("//span[contains(text(),'联系人：')]/..//text()").extract())
                item["phone"] = ''
                item["E_Mail"] = ''
                item["contact_Fax"] = ''
                item["contact_QQ"] = ''
                item["Source"] = response.url
                contact_infos = "".join(response.xpath("//span[contains(text(),'联系电话：')]/..//text()").extract())

                if item["company_Name"]:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|·公司名称：', '', item["company_Name"])\
                        .replace(' ','').strip()
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营产品：', '', item["kind"])\
                        .replace('-', '|').replace(
                        '、', '|') \
                        .replace('，', '|').replace('，', '|').replace('.', '').strip()
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
                else:
                    try:
                        item["linkman"] = "".join(re.findall(pattern1, response.text)) \
                            if re.findall(pattern1,response.text) else ''
                    except:
                        item["linkman"] = ''
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if contact_infos:
                    try:
                        item["phone"] = self.cw.search_phone_num(contact_infos)
                    except:
                        item["phone"] = ''
                    try:
                        item["telephone"] = self.cw.search_telephone_num(contact_infos)
                    except:
                        item["telephone"] = ''
                else:
                    item["phone"] = ''
                    item["telephone"] = ''


                    # if item["phone"]:
                #     item["phone"] = item["phone"]
                # else:
                #     try:
                #         item["phone"] = "".join(re.findall(pattern4, response.text)) if re.findall(pattern4,
                #                                                                                    response.text) else ''
                #     except:
                #         item["phone"] = ''
                # item["phone"] = self.cw.search_phone_num(item["phone"])
                #
                # if item["telephone"]:
                #     item["telephone"] = item["telephone"]
                # else:
                #     try:
                #         item["telephone"] = "".join(re.findall(pattern2, response.text)) if re.findall(pattern2,
                #                                                                                        response.text) else ''
                #     except:
                #         item["telephone"] = ''
                # item["telephone"] = self.cw.search_telephone_num(item["telephone"])

                if item["contact_Fax"]:
                    item["contact_Fax"] = item["contact_Fax"]
                else:
                    try:
                        item["contact_Fax"] = "".join(re.findall(pattern2, response.text)) if re.findall(pattern3,
                                                                                                         response.text) else ''
                    except:
                        item["contact_Fax"] = ''
                item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

                if item["E_Mail"]:
                    item["E_Mail"] = self.cw.search_email(item["E_Mail"])
                else:
                    item["E_Mail"] = ''

                if item["contact_QQ"]:
                    item["contact_QQ"] = item["contact_QQ"]
                else:
                    item["contact_QQ"] = ''
                item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

                if item["company_address"]:
                    item["company_address"] = item["company_address"]
                else:
                    try:
                        item["company_address"] = "".join(re.findall(pattern5, response.text)) if re.findall(pattern5,
                                                                                                             response.text) else ''
                    except:
                        item["company_address"] = ''
                item["company_address"] = self.cw.search_address(item["company_address"])

                # if item["host_href"]:
                #     item["host_href"] = item["host_href"]
                # else:
                #     item["host_href"] = ''

                yield item



    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "nt114"])