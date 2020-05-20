# # -*- coding: utf-8 -*-
# import re
# import scrapy
# from hashlib import md5
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
# from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.items import ShangNiuWangItem
# # from scrapy_redis.spiders import RedisCrawlSpider
# from scrapy.cmdline import execute
#
#
#
# class ShangNiuWangSpider(CrawlSpider):
#     name = "snw"
#     allowed_domains = ['www.sn180.com']
#     start_urls = ['http://www.sn180.com/Company/']
#     cw = CleanWords()
#     # redis_key = "ksb:start_urls"
#
#     custom_settings = {
#         'DOWNLOAD_DELAY': 0.5,
#         'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
#         'DEFAULT_REQUEST_HEADERS': {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#             "Accept-Encoding": "gzip, deflate",
#             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#             # "Connection": "keep-alive",
#             # "Cookie": "Hm_lvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566177749; CCKF_visitor_id_92126=1219631166; yunsuo_session_verify=db1a03528b7dfe197918cf533946c447; bdshare_firstime=1566178685689; Hm_lpvt_dd0c9f5bb6bab19ccc2b13c4ec58552a=1566178686",
#             # "Host": "jamesni139.tybaba.com",
#             # "Referer": "http://jamesni139.tybaba.com/",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
#         },
#         'DOWNLOADER_MIDDLEWARES': {
#             'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
#             # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 420,
#         },
#         # 不验证SSL证书
#         # "DOWNLOAD_HANDLERS_BASE": {
#         #     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
#         #     'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
#         #     'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
#         #     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
#         # },
#         # "DOWNLOAD_HANDLERS": {
#         #     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError'},
#     }
#     # /c3847/p2/
#     rules = (
#         Rule(LinkExtractor(
#             allow=r".*",restrict_xpaths=("//div[@id='Cat_Tab1']//a[@class='cats_b1']")), follow=True),
#
#         Rule(LinkExtractor(
#             allow=r".*", restrict_xpaths=("//table[@id='datalist_Companys']//tr//div[@class='compline']//a")),follow=True),
#
#         Rule(LinkExtractor(
#             allow=r".*",restrict_xpaths=("//strong[contains(text(),'下一页')]/..")), follow=True),
#
#         Rule(LinkExtractor(
#             allow=r".*", restrict_xpaths=("//span[contains(text(),'联系我们')]/..")), callback='parse_items',follow=False),
#     )
#
#     def parse_items(self, response):
#         item = ShangNiuWangItem()
#         # pattern = re.compile(r'>联系人：(.*?)<',re.S)
#         # pattern1 = re.compile(r'>移动电话：(.*?)<',re.S)
#         # pattern2 = re.compile(r'>地址：(.*?)<',re.S)
#         item["company_Name"] = response.xpath("//strong[@class='companytitle']/text()").get()
#         item["kind"] = "".join(response.xpath("//td[contains(text(),'主营行业：')]/following-sibling::td/text()").getall())
#         item["company_address"] = response.xpath("//b[contains(text(),'地　　址：')]/../following-sibling::td/span/text()").get()
#         item["linkman"] = response.xpath("//a[@id='namecard_linkman']/text()").get()
#         item["telephone"] = response.xpath("//b[contains(text(),'电　　话：')]/../following-sibling::td/text()").get()
#         item["phone"] = response.xpath("//b[contains(text(),'移动电话：')]/../following-sibling::td/text()").get()
#         item["contact_Fax"] = response.xpath("//b[contains(text(),'传　　真：')]/../following-sibling::td/text()").get()
#         item["contact_QQ"] = response.xpath("//img[@alt='给我发信息']/../@href").get()
#         item["E_Mail"] = response.xpath("//b[contains(text(),'邮　　箱：')]/../following-sibling::td/a/text()").get()
#         item["Source"] = response.url
#         item["province"] = ""
#         item["city_name"] = ""
#
#         if item["company_Name"]:
#             item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|企 业 名 称：', '', item["company_Name"]).replace(' ', '').strip()
#         item["company_id"] = self.get_md5(item["company_Name"])
#
#         if item["kind"]:
#             item["kind"] = item["kind"].replace(' ', '|')
#             item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
#                 .replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
#         else:
#             item["kind"] = ''
#
#         item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))
#
#         if item["linkman"]:
#             item["linkman"] = item["linkman"].replace("联 系 人：",'')
#         else:
#             item["linkman"] = response.xpath("//td[contains(text(),'企业法人')]/following-sibling::td/text()").get()
#         item["linkman"] = self.cw.search_linkman(item["linkman"])
#
#         if item["phone"]:
#             item["phone"] = item["phone"].replace("联 系 电 话：",'')
#             item["phone"] = self.cw.search_phone_num(item["phone"])
#         else:
#             item["phone"] = ''
#
#         if item["telephone"]:
#             item["telephone"] = item["telephone"].replace("联 系 电 话：",'')
#             item["telephone"] = self.cw.search_telephone_num(item["telephone"])
#         else:
#           item["telephone"] = ''
#
#         if item["contact_Fax"]:
#             item["contact_Fax"] = item["contact_Fax"].replace("公 司 传 真：",'')
#             item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
#         else:
#             item["contact_Fax"] = ''
#
#         if item["E_Mail"]:
#             item["E_Mail"] = item["E_Mail"].replace("电 子 邮 箱：",'')
#             item["E_Mail"] = self.cw.search_email(item["E_Mail"])
#         else:
#             item["E_Mail"] = ''
#
#         if item["contact_QQ"]:
#             item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
#         else:
#             try:
#                 item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
#             except:
#                 item["contact_QQ"] = ''
#
#         if item["company_address"]:
#             item["company_address"] = item["company_address"].replace('公 司 地 址：', '')
#             item["company_address"] = self.cw.search_address(item["company_address"])
#         else:
#             item["company_address"] = ''
#
#         yield item
#
#
#     def get_md5(self, value):
#         if value:
#             return md5(value.encode()).hexdigest()
#         return ''
#
#
#
#
# if __name__ == '__main__':
#     execute(["scrapy", "crawl", "snw"])