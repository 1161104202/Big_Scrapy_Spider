# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.data_tools.get_md5_hex import get_md5
from BigB2BSpider.items import ShangMaoTongspiderItem
from BigB2BSpider.data_tools.orc_img import recognition_image
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ShangMaoTongSpider(CrawlSpider):
    name = "smt"
    allowed_domains = ['b2bvip.com','www.b2bvip.com','www.fssandi.com']
    start_urls = ['http://companies.b2bvip.com/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566177749; CCKF_visitor_id_92126=1219631166; yunsuo_session_verify=db1a03528b7dfe197918cf533946c447; bdshare_firstime=1566178685689; Hm_lpvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566178686",
            # "Host": "jamesni139.tybaba.com",
            # "Referer": "http://jamesni139.tybaba.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 500,
        }
    }
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='bd']//li//a")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='main_content']//div[@class='list']//strong[@class='px14']/..")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='pages']//a[contains(text(),'下一页')]")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//span[contains(text(),'联系方式')]/..")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            # "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "UM_distinctid=16c327e51ab36a-06356b0f1a2259-3e385b04-1fa400-16c327e51ac406; Dlo_mysqlrw=-1; BAIDU_SSP_lcr=http://www.diqiuw.com/b2bwangzhandaquan/zonghepingtai/33439.html; PHPSESSID=p55subene36ad8nv9025ppf2t7; CNZZDATA1256887133=1877191215-1566200665-http%253A%252F%252Fcompanies.b2bvip.com%252F%7C1566200665; cck_lasttime=1566203362346; cck_count=0",
            # "Host": "chcsb6.b2bvip.com",
            "Referer": response.url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }
        pattern = re.compile(r'<meta name="keywords" content=".*?,(.*?)"/>',re.S)
        item = ShangMaoTongspiderItem()
        item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        item["company_address"] = response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/text()").extract_first()
        item["linkman"] = response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract_first()
        item["telephone"] = response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/img/@src").extract_first()
        item["phone"] = response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/img/@src").extract_first()
        item["contact_Fax"] = response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/img/@src").extract_first()
        item["contact_QQ"] = response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract_first()
        item["E_Mail"] = response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/img/@src").extract_first()
        item["Source"] = response.url
        item["kind"] = ",".join(response.xpath("//div[@class='side_class']//ul//li//a/text()").getall())
        item["province"] = ''
        item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = item["kind"].replace(" ",'|')
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace(' ', '|').replace('-', '|') \
                .replace('、', '|').replace('，', '|').replace(',', '|').replace('.', '|').strip()
        else:
            try:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = response.xpath("//div[@class='head']//h4/text()").extract_first()
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace(' ', '|').replace('-', '|') \
                    .replace('、', '|').replace('，', '|').replace(',', '|').replace('.', '|').strip()
            except:
                item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"]
        else:
            item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = self.requests_href(item["phone"], headers)
            item["phone"] = self.cw.search_phone_num(item["phone"])
        else:
            item["phone"] = ''

        if item["telephone"]:
            item["telephone"] = self.requests_href(item["telephone"], headers)
            item["telephone"] = self.cw.search_telephone_num(item["telephone"])
        else:
            item["telephone"] = ''

        if item["contact_Fax"]:
            item["contact_Fax"] = self.requests_href(item["contact_Fax"], headers)
            item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
        else:
            item["contact_Fax"] = ''

        if item["E_Mail"]:
            item["E_Mail"] = self.requests_href(item["E_Mail"], headers)
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
            something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img3\image.png"
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
    execute(["scrapy", "crawl", "smt"])