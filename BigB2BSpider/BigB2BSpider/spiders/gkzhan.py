# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from BigB2BSpider.data_tools.clean_worlds import CleanWords
# from BigB2BSpider.data_tools.orc_img import recognition_image
from BigB2BSpider.items import ZhiNengZhiZaoWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ZhiNengZhiZaoWangSpider(CrawlSpider):
    name = "gkzhan"
    allowed_domains = ['www.gkzhan.com','gkzhan.com']
    start_urls = ['https://www.gkzhan.com/company/a_t0/list_p0.html']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 420,
        },
    }
    # /c3847/p2/
    rules = (
        Rule(LinkExtractor(
            allow=r"\/st\d+",
            restrict_xpaths=("//div[@class='companylist']//p[@class='title']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//a[@class='lt']")), follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//ul//a[contains(text(),'联系我们')]")), callback="parse_items", follow=True),
    )



    def parse_items(self, response):
        item = ZhiNengZhiZaoWangItem()
        if response.text:
            try:
                if "初级榜上有名" in response.xpath("//div[@class='Grade']/img/@src").get():
                    pattern_cm = re.compile(r'<TITLE>联系我们－(.*?)</TITLE>',re.S)
                    pattern_kd = re.compile(r'<p>(.*?) - 主营产品： (.*?) </p>',re.S)
                    pattern_tp = re.compile(r'>\s*电话：(.*?)<br />', re.S)
                    pattern_ph = re.compile(r'>手机：(.*?)<br />', re.S)
                    pattern_fx = re.compile(r'>传真：(.*?)<br />', re.S)
                    pattern_lm = re.compile(r'>\s*联系人：(.*?)<br />', re.S)
                    pattern_lm1 = re.compile(r'<strong>联系人：(.*?)</strong>', re.S)
                    pattern_em = re.compile(r'>邮箱：(.*?)<br />', re.S)
                    pattern_add = re.compile(r'>\s*地址：(.*?)<br />', re.S)
                    pattern_area = re.compile(r'<p>所在省份：    (.*?)</p', re.S)
                    pattern_qq = re.compile(r'(\d+)@qq.com', re.S)

                    item["company_Name"] = "".join(re.findall(pattern_cm,response.text)[0]) if re.findall(pattern_cm,response.text) else ''
                    item["kind"] = "".join(re.findall(pattern_kd,response.text)[0][1]) if re.findall(pattern_kd,response.text) else ''
                    item["company_address"] = "".join(re.findall(pattern_add,response.text)[0]) if re.findall(pattern_add,response.text) else ''
                    item["linkman"] = "".join(re.findall(pattern_lm,response.text)[0]) if re.findall(pattern_lm,response.text) else ''
                    item["telephone"] = "".join(re.findall(pattern_tp,response.text)[0]) if re.findall(pattern_tp,response.text) else ''
                    item["phone"] = "".join(re.findall(pattern_ph,response.text)[0]) if re.findall(pattern_ph,response.text) else ''
                    item["contact_Fax"] = "".join(re.findall(pattern_fx,response.text)[0]) if re.findall(pattern_fx,response.text) else ''
                    item["contact_QQ"] = response.xpath("//a[@title='在线交流']/@href").get()
                    item["E_Mail"] = "".join(re.findall(pattern_em,response.text)[0]) if re.findall(pattern_em,response.text) else ''
                    item["Source"] = response.url
                    city_infos = "".join(re.findall(pattern_add,response.text)[0]) if re.findall(pattern_add,response.text) else ''

                    if item["company_Name"]:
                        item["company_Name"] = self.cw.search_company(item["company_Name"])
                    else:
                        try:
                            item["company_Name"] = "".join(re.findall(pattern_cm,response.text)) if re.findall(pattern_cm,response.text) else ''
                        except:
                            item["company_Name"] = ''
                    item["company_id"] = self.get_md5(item["company_Name"])

                    if item["kind"]:
                        item["kind"] = item["kind"].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                            .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
                    else:
                        try:
                            item["kind"] = response.xpath("//div[@class='gs']//h3/text()").get()
                            item["kind"] = item["kind"].replace(" ", '|')
                            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.',
                                                                                                                 '').strip()
                        except:
                            item["kind"] = ''
                    item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                    if item["linkman"]:
                        item["linkman"] = self.cw.search_linkman(item["linkman"])
                    else:
                        try:
                            item["linkman"] = "".join(re.findall(pattern_lm1,response.text)[0]) if re.findall(pattern_lm1,response.text) else ''
                        except:
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

                    if item["contact_QQ"]:
                        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
                    else:
                        item["contact_QQ"] = ''

                    if item["E_Mail"]:
                        item["E_Mail"] = self.cw.search_email(item["E_Mail"])
                    else:
                        try:
                            item["E_Mail"] = item["contact_QQ"] + "@qq.com"
                        except:
                            item["E_Mail"] = ''

                    if item["company_address"]:
                        item["company_address"] = item["company_address"].replace("联系地址：","")
                        item["company_address"] = self.cw.search_address(item["company_address"])
                    else:
                        item["company_address"] = ''

                    if city_infos:
                        if '市' and '省' in item["company_address"]:
                            try:
                                pattern_p = re.compile(r'(.*?)省', re.S)
                                pattern_c = re.compile(r'省(.*?)市', re.S)
                                item["province"] = "".join(re.findall(pattern_p, item["company_address"])) \
                                    if re.findall(pattern_p, item["company_address"]) else ''
                                item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                                    if re.findall(pattern_c, item["company_address"]) else ''
                            except:
                                item["province"] = ''
                                item["city_name"] = ''
                        else:
                            item["province"] = ''
                            item["city_name"] = ''
                    else:
                        item["province"] = ''
                        item["city_name"] = ''

                    yield item

                elif "中级榜上有名" in response.xpath("//div[@class='Grade']/img/@src").get():
                    pattern_cm = re.compile(r'<TITLE>联系我们－(.*?)</TITLE>', re.S)
                    pattern_kd = re.compile(r'<p>(.*?) - 主营产品： (.*?) </p>', re.S)
                    pattern_tp = re.compile(r'<p>电<b></b>话：    (.*?) </p>', re.S)
                    pattern_ph = re.compile(r'<p>手<b></b>机：    (.*?) </p>', re.S)
                    pattern_fx = re.compile(r'<p>传<b></b>真：    (.*?)</p>', re.S)
                    pattern_lm = re.compile(r'<p>联 系 人  ：  <i>(.*?)</i>', re.S)
                    pattern_lm1 = re.compile(r'<dt>联 系 人 ：</dt>\s*<dd><strong>(.*?)</strong>', re.S)
                    pattern_em = re.compile(r'<p>邮箱：    (.*?) </p>', re.S)
                    pattern_add = re.compile(r'<p>详细地址：    (.*?) </p>', re.S)
                    pattern_area = re.compile(r'<p>所在省份：    (.*?)</p', re.S)
                    pattern_qq = re.compile(r'(\d+)@qq.com', re.S)

                    item["company_Name"] = "".join(re.findall(pattern_cm, response.text)[0]) if re.findall(pattern_cm,
                                                                                                           response.text) else ''
                    item["kind"] = "".join(re.findall(pattern_kd, response.text)[0][1]) if re.findall(pattern_kd,
                                                                                                      response.text) else ''
                    item["company_address"] = "".join(re.findall(pattern_add, response.text)[0]) if re.findall(pattern_add,
                                                                                                               response.text) else ''
                    item["linkman"] = "".join(re.findall(pattern_lm, response.text)[0]) if re.findall(pattern_lm,
                                                                                                      response.text) else ''
                    item["telephone"] = "".join(re.findall(pattern_tp, response.text)[0]) if re.findall(pattern_tp,
                                                                                                        response.text) else ''
                    item["phone"] = "".join(re.findall(pattern_ph, response.text)[0]) if re.findall(pattern_ph,
                                                                                                    response.text) else ''
                    item["contact_Fax"] = "".join(re.findall(pattern_fx, response.text)[0]) if re.findall(pattern_fx,
                                                                                                          response.text) else ''
                    item["contact_QQ"] = response.xpath("//a[@title='在线交流']/@href").get()
                    item["E_Mail"] = "".join(re.findall(pattern_em, response.text)[0]) if re.findall(pattern_em,
                                                                                                     response.text) else ''
                    item["Source"] = response.url
                    city_infos = "".join(re.findall(pattern_add, response.text)[0]) if re.findall(pattern_add,
                                                                                                  response.text) else ''

                    if item["company_Name"]:
                        item["company_Name"] = self.cw.search_company(item["company_Name"])
                    else:
                        try:
                            item["company_Name"] = "".join(re.findall(pattern_cm, response.text)) if re.findall(pattern_cm,
                                                                                                                response.text) else ''
                        except:
                            item["company_Name"] = ''
                    item["company_id"] = self.get_md5(item["company_Name"])

                    if item["kind"]:
                        item["kind"] = item["kind"].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                            .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
                    else:
                        try:
                            item["kind"] = response.xpath("//div[@class='gs']//h3/text()").get()
                            item["kind"] = item["kind"].replace(" ", '|')
                            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                                .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.',
                                                                                                                 '').strip()
                        except:
                            item["kind"] = ''
                    item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                    if item["linkman"]:
                        item["linkman"] = self.cw.search_linkman(item["linkman"])
                    else:
                        try:
                            item["linkman"] = "".join(re.findall(pattern_lm1, response.text)[0]) if re.findall(pattern_lm1,
                                                                                                               response.text) else ''
                        except:
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

                    if item["contact_QQ"]:
                        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])
                    else:
                        item["contact_QQ"] = ''

                    if item["E_Mail"]:
                        item["E_Mail"] = self.cw.search_email(item["E_Mail"])
                    else:
                        try:
                            item["E_Mail"] = item["contact_QQ"] + "@qq.com"
                        except:
                            item["E_Mail"] = ''

                    if item["company_address"]:
                        item["company_address"] = item["company_address"].replace("联系地址：", "")
                        item["company_address"] = self.cw.search_address(item["company_address"])
                    else:
                        item["company_address"] = ''

                    if city_infos:
                        if '市' and '省' in item["company_address"]:
                            try:
                                pattern_p = re.compile(r'(.*?)省', re.S)
                                pattern_c = re.compile(r'省(.*?)市', re.S)
                                item["province"] = "".join(re.findall(pattern_p, item["company_address"])) \
                                    if re.findall(pattern_p, item["company_address"]) else ''
                                item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                                    if re.findall(pattern_c, item["company_address"]) else ''
                            except:
                                item["province"] = ''
                                item["city_name"] = ''
                        else:
                            item["province"] = ''
                            item["city_name"] = ''
                    else:
                        item["province"] = ''
                        item["city_name"] = ''

                    yield item

                elif "高级榜上有名" in response.xpath("//div[@class='Grade']/img/@src").get():
                    pattern_cm = re.compile(r'<<TITLE>联系我们－(.*?)</TITLE>', re.S)
                    pattern_kd = re.compile(r'<p>(.*?) - 主营产品： (.*?) </p>', re.S)
                    pattern_tp = re.compile(r'<dl><dt>电<b class="bcss"></b>话：</dt><dd>(.*?)&nbsp;</dd></dl>', re.S)
                    pattern_ph = re.compile(r'<dl><dt>手<b class="bcss"></b>机：</dt><dd>(.*?)&nbsp;</dd></dl>', re.S)
                    pattern_fx = re.compile(r'<dl><dt>传<b class="bcss"></b>真：</dt><dd>(.*?)&nbsp;</dd></dl>', re.S)
                    pattern_lm = re.compile(r'<div class="contact-person">\s*<img src=".*?" />(.*?)</div>', re.S)
                    # pattern_lm1 = re.compile(r'<strong>联系人：(.*?)</strong>', re.S)
                    pattern_em = re.compile(r'<dl><dt>邮<b class="bcss"></b>箱：</dt><dd>(.*?)&nbsp;</dd></dl>', re.S)
                    pattern_add = re.compile(r'<dl><dt>详细地址：</dt><dd>(.*?)&nbsp;</dd></dl>', re.S)
                    pattern_area = re.compile(r'<p>所在省份：    (.*?)</p', re.S)
                    pattern_qq = re.compile(r'(\d+)@qq.com', re.S)

                    item["company_Name"] = "".join(re.findall(pattern_cm, response.text)[0]) if re.findall(pattern_cm,response.text) else ''
                    item["kind"] = ",".join(response.xpath("//div[@class='prolist']//ul//li//a//text()").getall())
                    item["company_address"] = "".join(re.findall(pattern_add, response.text)[0]) if re.findall(pattern_add,response.text) else ''
                    item["linkman"] = "".join(re.findall(pattern_lm, response.text)[0]) if re.findall(pattern_lm,response.text) else ''
                    item["telephone"] = "".join(re.findall(pattern_tp, response.text)[0]) if re.findall(pattern_tp,response.text) else ''
                    item["phone"] = "".join(re.findall(pattern_ph, response.text)[0]) if re.findall(pattern_ph,response.text) else ''
                    item["contact_Fax"] = "".join(re.findall(pattern_fx, response.text)[0]) if re.findall(pattern_fx,response.text) else ''
                    item["contact_QQ"] = response.xpath("//a[@title='在线交流']/@href").get()
                    item["E_Mail"] = "".join(re.findall(pattern_em, response.text)[0]) if re.findall(pattern_em,response.text) else ''
                    item["Source"] = response.url
                    city_infos = "".join(re.findall(pattern_add, response.text)[0]) if re.findall(pattern_add,response.text) else ''

                    if item["company_Name"]:
                        item["company_Name"] = self.cw.search_company(item["company_Name"])
                    else:
                        try:
                            item["company_Name"] = "".join(re.findall(pattern_cm, response.text)) if re.findall(pattern_cm,
                                                                                                                response.text) else ''
                        except:
                            item["company_Name"] = ''
                    item["company_id"] = self.get_md5(item["company_Name"])

                    if item["kind"]:
                        item["kind"] = item["kind"].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                            .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
                    else:
                        item["kind"] = ''

                    item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                    if item["linkman"]:
                        item["linkman"] = self.cw.search_linkman(item["linkman"])
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
                        item["company_address"] = item["company_address"].replace("联系地址：", "")
                        item["company_address"] = self.cw.search_address(item["company_address"])
                    else:
                        item["company_address"] = ''

                    if city_infos:
                        if '市' and '省' in item["company_address"]:
                            try:
                                pattern_p = re.compile(r'(.*?)省', re.S)
                                pattern_c = re.compile(r'省(.*?)市', re.S)
                                item["province"] = "".join(re.findall(pattern_p, item["company_address"])) \
                                    if re.findall(pattern_p, item["company_address"]) else ''
                                item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                                    if re.findall(pattern_c, item["company_address"]) else ''
                            except:
                                item["province"] = ''
                                item["city_name"] = ''
                        else:
                            item["province"] = ''
                            item["city_name"] = ''
                    else:
                        item["province"] = ''
                        item["city_name"] = ''

                    yield item

                else:
                    pattern_cm = re.compile(r'<TITLE>联系我们－(.*?)</TITLE>', re.S)
                    pattern_kd = re.compile(r'<p>(.*?) - 主营产品： (.*?) </p>', re.S)
                    pattern_tp = re.compile(r'<p>电<b></b>话：    (.*?) </p>', re.S)
                    pattern_ph = re.compile(r'<p>手<b></b>机：    (.*?) </p>', re.S)
                    pattern_fx = re.compile(r'<p>传<b></b>真：    (.*?) </p>', re.S)
                    pattern_lm = re.compile(r'>\s*联系人：(.*?)<br />', re.S)
                    pattern_lm1 = re.compile(r'<strong>联系人：(.*?)</strong>', re.S)
                    pattern_em = re.compile(r'<p>邮<b></b>箱：    (.*?) </p>', re.S)
                    pattern_add = re.compile(r'<p>详细地址：    (.*?) </p>', re.S)
                    pattern_area = re.compile(r'<p>所在省份：    (.*?)</p', re.S)
                    pattern_qq = re.compile(r'(\d+)@qq.com', re.S)

                    item["company_Name"] = "".join(re.findall(pattern_cm, response.text)[0]) if re.findall(pattern_cm,
                                                                                                           response.text) else ''
                    item["kind"] = "".join(re.findall(pattern_kd, response.text)[0][1]) if re.findall(pattern_kd,
                                                                                                      response.text) else ''
                    item["company_address"] = "".join(re.findall(pattern_add, response.text)[0]) if re.findall(pattern_add,
                                                                                                               response.text) else ''
                    item["linkman"] = "".join(re.findall(pattern_lm, response.text)[0]) if re.findall(pattern_lm,
                                                                                                      response.text) else ''
                    item["telephone"] = "".join(re.findall(pattern_tp, response.text)[0]) if re.findall(pattern_tp,
                                                                                                        response.text) else ''
                    item["phone"] = "".join(re.findall(pattern_ph, response.text)[0]) if re.findall(pattern_ph,
                                                                                                    response.text) else ''
                    item["contact_Fax"] = "".join(re.findall(pattern_fx, response.text)[0]) if re.findall(pattern_fx,
                                                                                                          response.text) else ''
                    item["contact_QQ"] = response.xpath("//a[@title='在线交流']/@href").get()
                    item["E_Mail"] = "".join(re.findall(pattern_em, response.text)[0]) if re.findall(pattern_em,
                                                                                                     response.text) else ''
                    item["Source"] = response.url
                    city_infos = "".join(re.findall(pattern_add, response.text)[0]) if re.findall(pattern_add,
                                                                                                  response.text) else ''

                    if item["company_Name"]:
                        item["company_Name"] = self.cw.search_company(item["company_Name"])
                    else:
                        try:
                            item["company_Name"] = "".join(re.findall(pattern_cm, response.text)) if re.findall(pattern_cm,
                                                                                                                response.text) else ''
                        except:
                            item["company_Name"] = ''
                    item["company_id"] = self.get_md5(item["company_Name"])

                    if item["kind"]:
                        item["kind"] = item["kind"].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                            .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
                    else:
                        item["kind"] = ''

                    item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                    if item["linkman"]:
                        item["linkman"] = self.cw.search_linkman(item["linkman"])
                    else:
                        try:
                            item["linkman"] = "".join(re.findall(pattern_lm1, response.text)[0]) if re.findall(pattern_lm1,
                                                                                                               response.text) else ''
                        except:
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
                        item["company_address"] = item["company_address"].replace("联系地址：", "")
                        item["company_address"] = self.cw.search_address(item["company_address"])
                    else:
                        item["company_address"] = ''

                    if city_infos:
                        if '市' and '省' in item["company_address"]:
                            try:
                                pattern_p = re.compile(r'(.*?)省', re.S)
                                pattern_c = re.compile(r'省(.*?)市', re.S)
                                item["province"] = "".join(re.findall(pattern_p, item["company_address"])) \
                                    if re.findall(pattern_p, item["company_address"]) else ''
                                item["city_name"] = "".join(re.findall(pattern_c, item["company_address"])) \
                                    if re.findall(pattern_c, item["company_address"]) else ''
                            except:
                                item["province"] = ''
                                item["city_name"] = ''
                        else:
                            item["province"] = ''
                            item["city_name"] = ''
                    else:
                        item["province"] = ''
                        item["city_name"] = ''

                    yield item
            except:
                return



    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''

    # def requests_href(self, url, headers):
    #     res = requests.get(url=url, headers=headers, timeout=10, verify=False)
    #     res.encoding = "utf-8"
    #     if res.status_code == requests.codes.ok:
    #         img = res.content
    #         something_img_file_path = r"F:\PythonProjects\venv\pythonProjects\BigB2BSpider\BigB2BSpider\img_src\something_img3\image.png"
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
    execute(["scrapy", "crawl", "gkzhan"])