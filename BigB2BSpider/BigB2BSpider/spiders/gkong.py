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
from BigB2BSpider.items import ZhongHuaGongKongWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ZhongHuaGongKongWangSpider(CrawlSpider):
    name = "gkong"
    allowed_domains = ['www.gkong.com','gkong.com']
    start_urls = ['http://www.gkong.com/products/']
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

    def parse(self, response):
        kind_list = response.xpath("//a[@class='font04']")
        for k in kind_list:
            kind_name = k.xpath("./text()").get()
            kind_href = k.xpath("./@href").get()
            if kind_name:
                detail_href = "http://s.gkong.com/sEnterprise.aspx?q={}".format(kind_name)
                if detail_href:
                    yield scrapy.Request(
                        url=detail_href,
                        callback=self.parse_company_list,
                        dont_filter=True
                    )

    def parse_company_list(self, response):
        a_list = response.xpath("//div[@class='ResultHitsComm']//div//span[@class='result_title']//a")
        for a in a_list:
            company_Name = a.xpath(".//text()").getall()
            company_href = a.xpath("./@href").get()
            if company_href:
                yield scrapy.Request(
                    url=company_href,
                    callback=self.parse_items,
                    dont_filter=True
                )
        next_page_url = response.xpath("//a[contains(text(),'下一页>')]/@href").get()
        if next_page_url:
            next_page_url = "http://s.gkong.com/" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list,
                dont_filter=True
            )

    def parse_items(self, response):
        item = ZhongHuaGongKongWangItem()
        pattern = re.compile(r'<TD align=right nowrap class="padding5">'
                             r'区 域：</TD>\s*<TD class="padding5">.*?&nbsp;(.*?)&nbsp;(.*?)&nbsp;.*?</TD>',re.S)
        item["company_Name"] = response.xpath("///td[contains(text(),'全 称：')]/following-sibling::td/text()").extract_first()
        item["kind"] = "".join(response.xpath("//strong[contains(text(),'为:')]/..//text()").getall())
        item["company_address"] = response.xpath("//td[contains(text(),'地 址：')]/following-sibling::td/text()").extract_first()
        item["linkman"] = response.xpath("//td[contains(text(),'联系人：')]/following-sibling::td/text()").extract_first()
        item["telephone"] = response.xpath("//td[contains(text(),'电 话：')]/following-sibling::td/text()").extract_first()
        item["phone"] = response.xpath("//td[contains(text(),'手 机：')]/following-sibling::td/text()").extract_first()
        item["contact_Fax"] = "".join(response.xpath("//td[contains(text(),'传 真：')]/following-sibling::td//text()").extract())
        item["contact_QQ"] = response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract_first()
        item["E_Mail"] = response.xpath("//td[contains(text(),'邮 箱：')]/following-sibling::td/text()").extract_first()
        item["Source"] = response.url
        item["province"] = "".join(re.findall(pattern,response.text)[0][0]) if re.findall(pattern,response.text) else ''
        item["city_name"] = "".join(re.findall(pattern,response.text)[0][1]) if re.findall(pattern,response.text) else ''
        # city_infos = response.xpath("//td[contains(text(),'区 域：')]/following-sibling::td/text()").get()


        if item["company_Name"]:
            item["company_Name"] = self.cw.search_company(item["company_Name"])
        else:
            item["company_Name"] = ''
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            # '所分销产品为:PLC 可编程控制器 变频器与传动 伺服步进运动控制 人机界面 传感器 仪器仪表 工业以太网 PC based 工控机 低压电器 电源 FA&数控设备 机柜箱体 流体控制 工业安全 其它 '
            if ":" in item["kind"]:
                item["kind"] = item["kind"].split(':')[-1]
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：|生产产品为:|其它', '', item["kind"])\
                    .replace('-', '|').replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|')\
                    .replace('.', '').strip()
            else:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：|生产产品为:|其它', '', item["kind"]) \
                    .replace('-', '|').replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|') \
                    .replace('.', '').strip()
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
            item["company_address"] = item["company_address"].replace("联系地址：","")
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''

        # if city_infos:
        #     if '&nbsp;' in city_infos:
        #         try:
        #             item["province"] = city_infos.split('&nbsp;')[1]
        #             item["city_name"] = city_infos.split('&nbsp;')[2]
        #         except:
        #             item["province"] = ''
        #             item["city_name"] = ''
        #     else:
        #         item["province"] = ''
        #         item["city_name"] = ''
        # else:
        #     item["province"] = ''
        #     item["city_name"] = ''

        yield item

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
    execute(["scrapy", "crawl", "gkong"])