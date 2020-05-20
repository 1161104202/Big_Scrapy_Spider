# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import ErWuBaWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ErWuBaWangSpider(CrawlSpider):
    name = "ewb"
    allowed_domains = ['258.com','www.258.com','shop.258.com']
    start_urls = ['http://www.258.com/company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            # "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566177749; CCKF_visitor_id_92126=1219631166; yunsuo_session_verify=db1a03528b7dfe197918cf533946c447; bdshare_firstime=1566178685689; Hm_lpvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566178686",
            # "Host": "jamesni139.tybaba.com",
            # "Referer": "http://jamesni139.tybaba.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 420,
        },
        # 不验证SSL证书
        # "DOWNLOAD_HANDLERS_BASE": {
        #     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
        #     'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
        #     'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
        #     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
        # },
        # "DOWNLOAD_HANDLERS": {
        #     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'},
    }


    def parse(self, response):
        a_list = response.xpath("//li[@class='relative']//div[@class='ProductIndexRightNav']//li//a")
        for a in a_list:
            kind_href = a.xpath("./@href").get()
            kind_name = a.xpath("./text()").get()
            if kind_href:
                kind_href = "http://www.258.com" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        div_list = response.xpath("//div[@class='ovh mt10 ']//div[@class='qyk_sublistleft iconboxAll ']")
        for div in div_list:
            company_Name = div.xpath(".//h3/a/text()").get()
            company_href = div.xpath(".//h3/a/@href").get()
            kind = div.xpath("//span[contains(text(),'主营产品：')]/../text()").get()
            if company_href:
                yield scrapy.Request(
                    url=company_href,
                    callback=self.parse_company_detail,
                    dont_filter=True
                )
        # $.goToPage(4,this,'/Company/getList/cg/92/p/4')
        next_url = response.xpath("//a[contains(text(),'下一页')]/@onclick").get()
        pattern = re.compile(r"\$\.goToPage\(\d+,this,'(.*?)'\)", re.S)
        try:
            url = "".join(re.findall(pattern, next_url))
            if url:
                url = url.replace("getList/cg/", '')
                next_page_url = "http://www.258.com" + url
                if next_page_url:
                    yield scrapy.Request(
                        url=next_page_url,
                        callback=self.parse_company_list,
                        dont_filter=True
                    )
        except:
            return


    def parse_company_detail(self, response):
        contact_href = response.xpath("//a[contains(text(),'联系方式')]/@href").get()
        if contact_href:
            yield scrapy.Request(
                url=contact_href,
                callback=self.parse_company_contact,
                dont_filter=True
            )

    def parse_company_contact(self, response):
        pattern = re.compile(r'<span class="cp-name">(.*?)</span>',re.S)
        pattern1 = re.compile(r'>联系人：(.*?) <',re.S)
        pattern2 = re.compile(r'>QQ：(.*?)<', re.S)
        pattern3 = re.compile(r'>电话：(.*?)<', re.S)
        pattern4 = re.compile(r'>手机：(.*?)<', re.S)
        pattern5 = re.compile(r'>传真：(.*?)<', re.S)
        pattern6 = re.compile(r'>邮箱：(.*?)<', re.S)
        pattern7 = re.compile(r'>地址：(.*?)\s*<', re.S)
        pattern8 = re.compile(r'<input type="hidden" id="business_address" value="(.*?)" />', re.S)
        pattern9 = re.compile(r'>主营产品：(.*?)<', re.S)
        # pattern10 = re.compile(r'>所在地区：上海市 市辖区<')
        item = ErWuBaWangItem()
        if response.text:
            try:
                item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
                item["kind"] = "".join(re.findall(pattern9,response.text)) if re.findall(pattern9,response.text) else ''
                item["company_address"] = "".join(re.findall(pattern7,response.text)[0]) if re.findall(pattern7,response.text) else ''
                item["linkman"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
                item["telephone"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
                item["phone"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
                item["contact_Fax"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
                item["contact_QQ"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
                item["E_Mail"] = "".join(re.findall(pattern6,response.text)) if re.findall(pattern6,response.text) else ''
                item["Source"] = response.url
                item["province"] = ""
                item["city_name"] = ""

                if item["company_Name"]:
                    item["company_Name"] = re.sub(
                        r'\n|\s|\r|\t|公司名称：|企 业 名 称：', '', item["company_Name"]).replace(' ', '').strip()
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    if "主营产品" in item["kind"]:
                        item["kind"] = item["kind"].split('主营产品：')[-1]
                        item["kind"] = item["kind"].replace(' ', '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"])\
                            .replace('-', '|').replace('、','|').replace(',', '|').replace('，', '|')\
                            .replace(';', '|').replace('.', '').strip()
                    else:
                        item["kind"] = item["kind"]
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品:', '', item["kind"]) \
                            .replace('-', '|').replace('、', '|').replace(',', '|').replace('，', '|') \
                            .replace(';', '|').replace('.', '').strip()
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"].replace("联 系 人：",'')
                else:
                    item["linkman"] = ''
                item["linkman"] = self.cw.search_linkman(item["linkman"])

                if item["phone"]:
                    item["phone"] = item["phone"].replace("联 系 电 话：",'')
                    item["phone"] = self.cw.search_phone_num(item["phone"])
                else:
                    item["phone"] = ''

                if item["telephone"]:
                    item["telephone"] = item["telephone"].replace("联 系 电 话：",'')
                    item["telephone"] = self.cw.search_telephone_num(item["telephone"])
                else:
                  item["telephone"] = ''

                if item["contact_Fax"]:
                    item["contact_Fax"] = item["contact_Fax"].replace("公 司 传 真：",'')
                    item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
                else:
                    item["contact_Fax"] = ''

                if item["E_Mail"]:
                    item["E_Mail"] = item["E_Mail"].replace("电 子 邮 箱：",'')
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
                    item["company_address"] = item["company_address"].replace('公 司 地 址：', '')
                    item["company_address"] = self.cw.search_address(item["company_address"])
                else:
                    item["company_address"] = ''

                yield item

            except:
                return


    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "ewb"])