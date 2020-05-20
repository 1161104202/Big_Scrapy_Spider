# # -*- coding: utf-8 -*-
# import re
# import scrapy
# from hashlib import md5
# from scrapy.spiders import CrawlSpider, Rule
# from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.items import Bigb2BspiderItem
# from scrapy.cmdline import execute
#
#
#
# class JiancaiSpider(CrawlSpider):
#     name = 'jiancai'
#     allowed_domains = ['www.jiancai.com']
#     start_urls = ['http://www.jiancai.com/corporation/']
#     cw = CleanWords()
#
#
#     def parse(self, response):
#         a_list = response.xpath("//div[@class='TabContent']//table[@valign='top']//tr//td//a")
#         for a in a_list:
#             kind_name = a.xpath("./text()").extract_first()
#             kind_href = a.xpath("./@href").extract_first()
#             if kind_href:
#                 kind_href = "http://www.jiancai.com" + kind_href
#                 # print(kind_name,kind_href)
#                 yield scrapy.Request(
#                     url=kind_href,
#                     callback=self.parse_company_list,
#                     dont_filter=True
#                 )
#
#     def parse_company_list(self, response):
#         div_list = response.xpath("//div[@id='divFloatDilog']//div[@class='left02']//a[1]")
#         for div in div_list:
#             company_Name = "".join(div.xpath("./text").extract())
#             company_href = div.xpath("./@href").extract_first()
#             if company_href:
#                 # print(company_Name,company_href)
#                 yield scrapy.Request(
#                     url=company_href,
#                     callback=self.parse_company_contact,
#                     meta={"info": company_Name},
#                     dont_filter=True
#                 )
#
#             next_page_url = response.xpath("//div[@class='listpage']//a[contains(text(),'下一页')]").extract_first()
#             if next_page_url:
#                 next_page_url = "http://www.jiancai.com/corporation/trade/" + next_page_url
#                 yield scrapy.Request(
#                     url=next_page_url,
#                     callback=self.parse_company_list
#                 )
#
#     def parse_company_contact(self, response):
#         item = Bigb2BspiderItem()
#         pattern = re.compile(r'<meta name="keywords" content="(.*?)" />',re.S)
#         pattern1 = re.compile(r'<li>主营产品： (.*?)</li>', re.S)
#         pattern2 = re.compile(r'<li>所在地区：(.*?)</li>', re.S)
#         pattern3 = re.compile(r'<li>联系人：(.*?)</li>', re.S)
#         pattern4 = re.compile(r'<li>手机：(.*?)</li>', re.S)
#         pattern5 = re.compile(r'<li>联系电话：(.*?)</li>', re.S)
#         pattern6 = re.compile(r'<li>公司传真：(.*?)</li>', re.S)
#         pattern7 = re.compile(r'href="tencent://message/?Site=jiancai.com&amp;Uin=(.*?)&amp;Menu=yes"',re.S)
#         pattern8 = re.compile(r'>\s*联系人：(.*?)</li>',re.S)
#
#         item["company_Name"] = "".join(re.findall(pattern,response.text)) if response.text else ''
#         # item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
#         item["kind"] = "|".join(response.xpath("//div[@id='enname']/text()").extract())
#         item["company_address"] = "".join(response.xpath("//td[contains(text(),'公司地址:')]/following-sibling::td/text()").extract())
#         item["linkman"] = "".join(re.findall(pattern8,response.text) if response.text else '')
#         item["telephone"] = "".join(response.xpath("//div[@class='ContCnt']//li[3]/text()").extract())
#         item["phone"] = "".join(response.xpath("//div[@class='ContCnt']//li[4]/text()").extract())
#         item["contact_Fax"] = "".join(response.xpath("//div[@class='ContCnt']//li[5]/text()").extract())
#         item["contact_QQ"] = "".join(response.xpath("//div[@class='ContCnt']//li[2]//a/@href").extract())
#         item["Source"] = response.url
#
#         if item["company_Name"]:
#             item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
#         item["company_id"] = self.get_md5(item["company_Name"])
#
#         if item["kind"]:
#             item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：', '', item["kind"]).replace('、', '|') \
#                 .replace('，', '|').replace('，', '|').replace('.', '').strip()
#         else:
#             try:
#                 item["kind"] = "".join(re.findall(pattern1,response.text) if response.text else '')
#                 item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：', '', item["kind"]).replace('、', '|') \
#                 .replace('，', '|').replace('，', '|').replace('.', '').strip()
#             except:
#                 return ''
#         item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))
#
#         if item["linkman"]:
#             item["linkman"] = item["linkman"]
#         else:
#             try:
#                 item["linkman"] = "".join(re.findall(pattern3,response.text) if response.text else '')
#             except:
#                 return ''
#         item["linkman"] = self.cw.search_linkman(item["linkman"])
#
#         if item["phone"]:
#             item["phone"] = item["phone"]
#         else:
#             try:
#                 item["phone"] = "".join(re.findall(pattern4,response.text) if response.text else '')
#             except:
#                 return ''
#         item["phone"] = self.cw.search_phone_num(item["phone"])
#
#         if item["telephone"]:
#             item["telephone"] = item["telephone"]
#         else:
#             try:
#                 item["telephone"] = "".join(re.findall(pattern5,response.text) if response.text else '')
#             except:
#                 return ''
#         item["telephone"] = self.cw.search_telephone_num(item["telephone"])
#
#         if item["contact_Fax"]:
#             item["contact_Fax"] = item["contact_Fax"]
#         else:
#             try:
#                 item["contact_Fax"] = "".join(re.findall(pattern6,response.text) if response.text else '')
#             except:
#                 return ''
#         item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])
#
#         # if item["E_Mail"]:
#         #     item["E_Mail"] = self.cw.search_QQ(item["E_Mail"])
#         # else:
#         #     item["E_Mail"] = ''
#
#         if item["contact_QQ"]:
#             item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
#         else:
#             try:
#                 item["contact_QQ"] = "".join(re.findall(pattern7,response.text) if response.text else '')
#             except:
#                 return ''
#         item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
#
#         if item["company_address"]:
#             item["company_address"] = item["company_address"]
#         else:
#             try:
#                 item["company_address"] = "".join(re.findall(pattern2,response.text) if response.text else '')
#             except:
#                 return ''
#         item["company_address"] = self.cw.search_address(item["company_address"])
#
#         # if item["host_href"]:
#         #     item["host_href"] = item["host_href"]
#         # else:
#         #     item["host_href"] = ''
#
#         yield item
#
#     def get_md5(self, value):
#         if value:
#             return md5(value.encode()).hexdigest()
#         return ''
#
#
# if __name__ == '__main__':
#     execute(["scrapy", "crawl", "jiancai"])