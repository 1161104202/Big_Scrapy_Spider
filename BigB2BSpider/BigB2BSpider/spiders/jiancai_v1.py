# # -*- coding: utf-8 -*-
# import scrapy
# from hashlib import md5
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.loader import ItemLoader
# from BigB2BSpider.items import Bigb2BspiderItem
#
#
#
# class JiancaiSpider(CrawlSpider):
#     name = 'jiancai'
#     allowed_domains = ['www.jiancai.com']
#     start_urls = ['http://www.jiancai.com/corporation/']
#
#     # linkextractor = LinkExtractor(allow=(r'/corporation/trade/\d+.html',))
#     # linkextractor1 = LinkExtractor(allow=r'/corporation/trade/\d+.html', restrict_xpaths=("//div[@class='TabContent']//table[@valign='top']//tr//td//a"))
#     # linkextractor2 = LinkExtractor(allow=r'http://.*?\.jiancai.com', restrict_xpaths=("//div[@id='divFloatDilog']//div[@class='left02']//a[1]"))
#     # linkextractor3 = LinkExtractor(allow=r'\d+\-p\d+.html', restrict_xpaths=("//div[@class='listpage']//a[contains(text(),'下一页')]",))
#     # rules = [
#     #     # 首页分类链接
#     #     Rule(linkextractor1,follow=True),
#     #     # 列表页公司链接
#     #     Rule(linkextractor2, callback="parse", follow=True),
#     #     # 翻页链接
#     #     Rule(linkextractor3, follow=True),
#     # ]
#
#     Rule(LinkExtractor(restrict_xpaths="//div[@class='TabContent']"),follow=True),  # 第一步
#     Rule(LinkExtractor(restrict_xpaths="//div[@class='TabContent']"), follow=True,callback='parse_item'),  # 第二步
#     Rule(LinkExtractor(restrict_xpaths="//div[@class='listpage']"), follow=True),  # 第三步翻翻页
#
#     # Rule(LinkExtractor(allow='/corporation/trade/\d+.html', restrict_xpaths="//div[@class='TabContent']"), follow=True),  # 第一步
#     # Rule(LinkExtractor(allow='http://.*?\.jiancai.com', restrict_xpaths="//div[@class='TabContent']"),follow=True,callback = 'parse_item'),  # 第二步
#     # Rule(LinkExtractor(allow="\d+\-p\d+.html", restrict_xpaths="//div[@class='listpage']"),follow=True),  # 第三步翻翻页
#     # Rule(LinkExtractor(allow="/subject/\d+/$",restrict_xpaths = "//ul[@class='subject-list']"), callback = 'parse_item')  # 得到所需网页的url
#
#
#
#     def parse_item(self, response):
#         item = Bigb2BspiderItem()
#         item["company_Name"] = "".join(response.css("#cnname > h1::attr(text)").extract())
#         item["company_id"] = md5(item["company_Name"].encode()).hexdigest()
#         item["kind"] = "|".join(response.css("#enname::attr(text)").extract())
#
#         item["linkman"] = "".join(response.css("#tableAbout > tbody > tr:nth-child(3) > td.cNameBgcolor::attr(text)").extract())
#         item["telephone"] = "".join(response.css("#tableAbout > tbody > tr:nth-child(4) > td:nth-child(2)::attr(text)").extract())
#         item["phone"] = "".join(response.css("#tableAbout > tbody > tr:nth-child(6) > td:nth-child(2)::attr(text)").extract())
#         item["contact_Fax"] = "".join(response.css("#tableAbout > tbody > tr:nth-child(5) > td:nth-child(2)::attr(text)").extract())
#         item["Source"] = response.url
#         yield item
#
#
#
#
#         # big_itemload = ItemLoader(item=Bigb2BspiderItem(), response=response)
#         # # company_Name = response.xpath("//")
#         # big_itemload.add_css("company_Name","#cnname > h1::attr(text)")
#         # # big_itemload.add_css("id", md5())
#         # big_itemload.add_css("kind", "#enname::attr(text)")
#         # big_itemload.add_css("linkman", "#tableAbout > tbody > tr:nth-child(3) > td.cNameBgcolor::attr(text)")
#         # big_itemload.add_css("telephone", "#tableAbout > tbody > tr:nth-child(4) > td:nth-child(2)::attr(text)")
#         # big_itemload.add_css("contact_Fax", "#tableAbout > tbody > tr:nth-child(5) > td:nth-child(2)::attr(text)")
#         # big_itemload.add_css("phone", "#tableAbout > tbody > tr:nth-child(6) > td:nth-child(2)::attr(text)")
#         # big_itemload.add_css("company_address", "#tableAbout > tbody > tr:nth-child(2) > td:nth-child(2)::attr(text)")
#         # big_itemload.add_css("Source", response.url)
#         #
#         # yield big_itemload.item()
#
