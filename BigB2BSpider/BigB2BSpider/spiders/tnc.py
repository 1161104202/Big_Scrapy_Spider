# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import QuanQiuFangZhiWangspiderItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class QuanQiuFangZhiWangSpider(CrawlSpider):
    name = "tnc"
    allowed_domains = ['tnc.com.cn','www.tnc.com.cn']
    start_urls = ['https://www.tnc.com.cn/company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Host": "www.kusoba.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        }
    }
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='area-list']//li//a")), follow=True),

        Rule(LinkExtractor(allow=r".*",restrict_xpaths=("//div[@class='result-list-company']//p[@class='tit']//a")), follow=True),

        Rule(LinkExtractor(allow=r".*",restrict_xpaths=("//a[@class='page-next']")), follow=True),

        Rule(LinkExtractor(allow=r".*",restrict_xpaths=("//a[contains(text(),'联系方式')]")),callback='parse_items', follow=False),
    )

    def parse_items(self, response):
        # print(response.text)
        # <title>Jill:-舟山达利针织有限公司联系方式--全球纺织网</title>
        # 		<meta name="keywords" content="舟山达利针织有限公司，Jill，" />
        # 		<meta name="description" content="舟山达利针织有限公司负责人：Jill，手机：，座机：-0580-8805716，传真：-0580-8805500，详细地址：定海区盐仓"/>
        # '舟山达利针织有限公司负责人：Jill，手机：，座机：-0580-8805716，传真：-0580-8805500，详细地址：定海区盐仓'
        pattern = re.compile(r'<div class="jbxx_zt">(.*?)</div>',re.S)
        pattern1 = re.compile(r'<p class="indouce">(.*?)</p>', re.S)
        pattern2 = re.compile(r'手机：(.*?)，', re.S)
        pattern3 = re.compile(r'座机：(.*?)，', re.S)
        pattern4 = re.compile(r'传真：(.*?)，', re.S)
        pattern5 = re.compile(r'详细地址：(.*)', re.S)
        pattern6 = re.compile(r'负责人：(.*?)，', re.S)
        pattern7 = re.compile(r'<meta name="description" content="(.*?)"/>',re.S)
        item = QuanQiuFangZhiWangspiderItem()
        if response.text:
            try:
                content = "".join(re.findall(pattern7,response.text)) if re.findall(pattern7,response.text) else ''
                item["company_Name"] = "".join(re.findall(pattern,response.text)) if re.findall(pattern,response.text) else ''
                item["kind"] = "".join(re.findall(pattern1,response.text)[0]) if re.findall(pattern1,response.text) else ''
                item["company_address"] = "".join(re.findall(pattern5,content)) if re.findall(pattern5,content) else ''
                item["linkman"] = "".join(re.findall(pattern6,content)) if re.findall(pattern6,content) else ''
                item["telephone"] = "".join(re.findall(pattern3,content)) if re.findall(pattern3,content) else ''
                item["phone"] = "".join(re.findall(pattern2,content)) if re.findall(pattern2,content) else ''
                item["contact_Fax"] = "".join(re.findall(pattern4,content)) if re.findall(pattern4,content) else ''
                item["contact_QQ"] = ""
                item["E_Mail"] = ""
                item["Source"] = response.url
                item["province"] = ""
                item["city_name"] = ""

                if item["company_Name"]:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|全称：', '', item["company_Name"]).replace(' ', '').strip()
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营产品：', '', item["kind"]).replace('-', '|').replace('、', '|') \
                        .replace('，', '|').replace('，', '|').replace('.', '').strip()
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    if "（" in item["linkman"]:
                        item["linkman"] = item["linkman"].split("（")[0].replace('法定代表人：','').replace('暂未公布','')
                    else:
                        item["linkman"] = item["linkman"].replace('法定代表人：','').replace('暂未公布','')
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
                    if "\"" in item["company_address"]:
                        item["company_address"] = item["company_address"].spilt('"')[0]
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
    execute(["scrapy", "crawl", "tnc"])