# -*- coding: utf-8 -*-
import re
import scrapy
import requests
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import WuYiSuoLeWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class WuYiSuoLeWangSpider(CrawlSpider):
    name = "sole51"
    allowed_domains = ['www.51sole.com','51sole.com']
    start_urls = ['http://www.51sole.com/company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
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
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='enterprise-info']//li//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='hy_include']//ul//li//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='hy_companylist']//li//span[@class='fl']//a")), callback='parse_items', follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("///div[@class='list-page']//a[contains(text(),'下一页')]")), follow=True),
    )

    def parse_items(self, response):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "UM_distinctid=16bcf23d2594d4-0684611a52deb5-3e385b04-1fa400-16bcf23d25a2de; Hm_lvt_5a1e76d3dd6018bc41c2d2ff155b54de=1566959342; Hm_lvt_a6bece9ed4ad299bd960f0b964fa848e=1566959374; Hm_lpvt_a6bece9ed4ad299bd960f0b964fa848e=1566959374; CompanyName=; MobilePhone=; PersonName=; AccountName=; ASP.NET_SessionId=0lmy5gymayy4ri3jrqcuchtv; bdshare_firstime=1566960266663; Hm_lpvt_5a1e76d3dd6018bc41c2d2ff155b54de=1566960424",
            "Host": "www.51sole.com",
            # "If-Modified-Since": "Wed, 28 Aug 2019 02:40:00 GMT",
            "Referer": response.url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }
        item = WuYiSuoLeWangItem()
        if "company/detail_" in response.url:
            pattern = re.compile(r'"<span>电话：(.*?)</span><br><span>地址：(.*?)</span>",',re.S)
            item["company_Name"] = response.xpath("//div[@class='profile-name']//span//text()").extract_first()
            item["kind"] = "".join(response.xpath("//em[contains(text(),'主营产品：')]/../..//text()").getall())
            item["company_address"] = response.xpath("//em[contains(text(),'址：')]/../text()").get()
            item["linkman"] = response.xpath("//em[contains(text(),'人：')]/../text()").extract_first()
            item["telephone"] = "".join(re.findall(pattern,response.text)[0][0]) if re.findall(pattern,response.text) else ''
            item["phone"] = response.xpath("//em[contains(text(),'话：')]/..//img/@src").extract_first()
            item["contact_Fax"] = ''
            item["contact_QQ"] = ''
            item["E_Mail"] = ''
            item["Source"] = response.url
            item["province"] = ""
            item["city_name"] = ""

            if item["company_Name"]:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(' ', '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品', '', item["kind"]).replace('-', '|').replace('、', '|') \
                    .replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            else:
                try:
                    item["kind"] = response.xpath("//em[contains(text(),'主营业务：')]/../text()").get()
                    item["kind"] = item["kind"].replace(' ', '|')
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品', '', item["kind"]).replace('-', '|')\
                        .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|')\
                        .replace('.', '').strip()
                except:
                    item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"]
            else:
                item["linkman"] = ''
            item["linkman"] = self.cw.search_linkman(item["linkman"])

            if item["phone"]:
                item["phone"] = "http://www.51sole.com" + item["phone"]
                item["phone"] = self.requests_href(item["phone"],headers)
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

            yield item
        else:
            pattern1 = re.compile(r'<li><i>地址：</i><span>(.*?)</span></li>',re.S)
            pattern2 = re.compile(r'<li><i>联系人：</i><span>(.*?)</span></li>', re.S)
            pattern3 = re.compile(r'<li><i>电话：</i><span>(.*?)</span></li>', re.S)
            pattern4 = re.compile(r'<li><i>手机：</i><span>(.*?)\s*</span></li>', re.S)
            pattern5 = re.compile(r'>主营产品：(.*?)<', re.S)

            item["company_Name"] = response.xpath("//div[@id='namelogo']//p/text()").get()
            item["kind"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
            item["company_address"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
            item["linkman"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
            item["telephone"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
            item["phone"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
            item["contact_Fax"] = ''
            item["contact_QQ"] = ''
            item["E_Mail"] = ''
            item["Source"] = response.url
            item["province"] = ""
            item["city_name"] = ""

            if item["company_Name"]:
                item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(' ', '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品', '', item["kind"]).replace('-', '|').replace('、', '|') \
                    .replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            else:
                try:
                    item["kind"] = response.xpath("//em[contains(text(),'主营业务：')]/../text()").get()
                    item["kind"] = item["kind"].replace(' ', '|')
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营产品', '', item["kind"]).replace('-', '|')\
                        .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|')\
                        .replace('.', '').strip()
                except:
                    item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"]
            else:
                item["linkman"] = ''
            item["linkman"] = self.cw.search_linkman(item["linkman"])

            if item["telephone"]:
                if item["telephone"].startswith("-"):
                    item["telephone"] = item["telephone"].split('-')[1:]
                else:
                    item["telephone"] = item["telephone"]
            else:
                item["telephone"] = ''
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])

            if item["phone"]:
                item["phone"] = self.cw.search_phone_num(item["phone"])
            else:
                try:
                    item["phone"] = self.cw.search_phone_num(item["telephone"])
                except:
                    item["phone"] = ''
            item["phone"] = self.cw.search_phone_num(item["phone"])

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

            yield item




    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''

    def requests_href(self, url, headers):
        res = requests.get(url=url, headers=headers, timeout=10, verify=False)
        res.encoding = "utf-8"
        if res.status_code == requests.codes.ok:
            img = res.content
            something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img1\image.png"
            with open(something_img_file_path, "wb") as fp:
                fp.write(img)
            fp.close()
            if img:
                try:
                    something = recognition_image(something_img_file_path)
                    if something:
                        return something
                    else:
                        return ''
                except:
                    return ''
            else:
                return ''
        else:
            return ''




if __name__ == '__main__':
    execute(["scrapy", "crawl", "sole51"])