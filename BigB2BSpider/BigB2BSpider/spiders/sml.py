# # -*- coding: utf-8 -*-
# import re
# import scrapy
# from hashlib import md5
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
# from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.items import ShangMingLuWangItem
# # from scrapy_redis.spiders import RedisCrawlSpider
# from scrapy.cmdline import execute
#
#
#
# class ShangMingLuWangSpider(CrawlSpider):
#     name = "sml"
#     allowed_domains = ['b2bname.com','www.b2bname.com']
#     start_urls = ['http://www.b2bname.com/area.php']
#     cw = CleanWords()
#     # redis_key = "ksb:start_urls"
#
#     custom_settings = {
#         'DOWNLOAD_DELAY': 0.5,
#         'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
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
#             allow=r".*",restrict_xpaths=("//div[@class='main mgline']//dl[@id='alllist']//dd//a")),follow=True),
#
#         Rule(LinkExtractor(
#             allow=r".*", restrict_xpaths=("//div[@class='main mgline']//div[@class='block-tab-item mgline']//ul//li//a")), follow=True),
#
#         Rule(LinkExtractor(
#             allow=r".*", restrict_xpaths=("//div[@class='pagebar']//b[contains(text(),'下一页')]/..")), follow=True),
#
#         Rule(LinkExtractor(
#             allow=r".*",restrict_xpaths=("//div[@class='pub-nav-c pub-fc']//a[contains(text(),'联系方式')]")),callback='parse_items',follow=True),
#
#     )
#
#     def parse_items(self, response):
#         item = ShangMingLuWangItem()
#         pattern = re.compile(r'(1\d{10})', re.S)
#         pattern1 = re.compile(r'<meta name="keywords" content=".*?_.*?;(.*?)"/>',re.S)
#         item["company_Name"] = response.xpath("//b[contains(text(),'单位名称:')]/../text()").extract_first()
#         item["kind"] = "|".join(re.findall(pattern1,response.text)[0]) if re.findall(pattern1,response.text) else ''
#         item["company_address"] = response.xpath("//b[contains(text(),'地址:')]/../text()").extract_first()
#         item["linkman"] = response.xpath("//b[contains(text(),'联系人:')]/../text()").extract_first()
#         item["telephone"] = ''
#         item["phone"] = "".join(re.findall(pattern,response.text)[0]) if re.findall(pattern,response.text) else ''
#         item["contact_Fax"] = response.xpath("//b[contains(text(),'传真:')]/../text()").extract_first()
#         item["contact_QQ"] = response.xpath("//b[contains(text(),'QQ:')]/../text()").extract_first()
#         item["E_Mail"] = response.xpath("//b[contains(text(),'邮箱:')]/../text()").extract_first()
#         item["Source"] = response.url
#         item["province"] = ""
#         item["city_name"] = ""
#
#         if item["company_Name"]:
#             if "（" in item["company_Name"]:
#                 item["company_Name"] = item["company_Name"].split('（')[0]
#             elif "(" in item["company_Name"]:
#                 item["company_Name"] = item["company_Name"].split('(')[0]
#             else:
#                 item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
#         item["company_id"] = self.get_md5(item["company_Name"])
#
#         if item["kind"]:
#             item["kind"] = item["kind"].replace(' ', '|')
#             item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|').replace('、', '|')\
#                 .replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
#         else:
#             item["kind"] = ''
#
#         item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))
#
#         if item["linkman"]:
#             if re.findall(r'(1\d+)', item["linkman"]):
#                 try:
#                     item["linkman"] = re.sub("".join(re.findall(r'(1\d+)', item["linkman"])),'',item["linkman"])
#                 except:
#                     item["linkman"] = ''
#         else:
#             item["linkman"] = ''
#         item["linkman"] = self.cw.search_linkman(item["linkman"])
#
#         if item["telephone"]:
#             item["telephone"] = item["telephone"]
#         else:
#           item["telephone"] = ''
#         item["telephone"] = self.cw.search_telephone_num(item["telephone"])
#
#         if item["phone"]:
#             item["phone"] = item["phone"]
#         else:
#             try:
#                 item["phone"] = self.cw.search_phone_num(item["telephone"])
#             except:
#                 item["phone"] = ''
#         item["phone"] = self.cw.search_phone_num(item["phone"])
#
#         if item["contact_Fax"]:
#             item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
#         else:
#             item["contact_Fax"] = ''
#
#         if item["E_Mail"]:
#             item["E_Mail"] = self.cw.search_email(item["E_Mail"])
#         else:
#             item["E_Mail"] = ''
#
#         if item["contact_QQ"]:
#             item["contact_QQ"] = item["contact_QQ"].replace("Q Q：",'')
#         else:
#             try:
#                 item["contact_QQ"] = "".join(re.findall(r'(\d+)@qq.com',item["E_Mail"])) \
#                     if re.findall(r'(\d+)@qq.com',item["E_Mail"]) else ''
#             except:
#                 item["contact_QQ"] = ''
#         item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
#
#         if item["company_address"]:
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
#     execute(["scrapy", "crawl", "sml"])