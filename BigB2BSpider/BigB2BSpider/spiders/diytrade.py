# -*- coding: utf-8 -*-
import re
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import ZiZhuMaoYiWangspiderItem
from scrapy.cmdline import execute



class ZiZhuMaoYiWangSpider(CrawlSpider):
    # 自助贸易网
    name = 'diytrade'
    allowed_domains = ['cn.diytrade.com','diytrade.com']
    start_urls = ['https://cn.diytrade.com/china/main.html']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,  # 延时最低为2s
        # 'AUTOTHROTTLE_ENABLED': True,  # 启动[自动限速]
        # 'AUTOTHROTTLE_DEBUG': True,  # 开启[自动限速]的debug
        # 'AUTOTHROTTLE_MAX_DELAY': 10,  # 设置最大下载延时
        'DOWNLOAD_TIMEOUT': 5, #设置下载超时
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5, # 限制对该网站的并发请求数
        'ITEM_PIPELINES': {'BigB2BSpider.pipelines.MysqlTwistedPiplines': 302},
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_34c005d4caf30d75012a05867beca619=1562747829,1564973957; Hm_lpvt_34c005d4caf30d75012a05867beca619=1564974049",
            # "Host": "b2b.huishangbao.com",
            # "Referer": "http://b2b.huishangbao.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
            # 'BigB2BSpider.middlewares.ProcessAllExceptionMiddleware': 120,
        }
    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='prodCatListDIV']//ul[@class='prodCatList']//li//a")
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_href:
                if kind_href.startswith("http://"):
                    kind_href = kind_href
                else:
                    kind_href = "https://cn.diytrade.com" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_kind_list,
                    dont_filter=True
                )

    def parse_kind_list(self, response):
        s_kind_href = response.xpath("//a[contains(text(),'» 公司信息')]/@href").extract_first()
        if s_kind_href:
            s_kind_href = "https://cn.diytrade.com" + s_kind_href
            yield scrapy.Request(
                url=s_kind_href,
                callback=self.parse_company_list,
                dont_filter=True
            )

    def parse_company_list(self, response):
        div_list = response.xpath("//form[@name='itemForm']//ul[@class='comItems']//li")
        for div in div_list:
            item = ZiZhuMaoYiWangspiderItem()
            item["company_Name"] = div.xpath(".//div[@class='col3']/h3/a/text()").extract_first()
            company_href = div.xpath(".//div[@class='col3']/h3/a/@href").extract_first()
            if company_href:
                # print(company_href)
                company_href = "https://cn.diytrade.com" + company_href
                # print(contact_href)
                yield scrapy.Request(
                    url=company_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        next_page_url = response.xpath("//div[@class='clearfix pageNavList']//a[contains(text(),'下一页')]/@href").extract_first()
        if next_page_url:
            next_page_url = "https://cn.diytrade.com" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    # def parse_company_detail(self, response):
    #     item = response.meta["item"]
    #     contact_href = response.xpath("//li//a[contains(text(),'联系我们')]/@href").extract_first()
    #     if contact_href:
    #         yield scrapy.Request(
    #             url=contact_href,
    #             callback=self.parse_company_contact,
    #             meta={"item": item},
    #             dont_filter=True
    #         )


    def parse_company_contact(self, response):
        item = response.meta["item"]
        pattern = re.compile(r'uin=(.*?)&',re.S)
        # item["company_Name"] = response.xpath("//th[contains(text(),'公司名称︰')]/following-sibling::td/text()").extract_first()
        item["kind"] = response.xpath("//th[contains(text(),'主营行业︰')]/following-sibling::td/h3/text()").extract_first()
        item["company_address"] = response.xpath("//th[contains(text(),'地址︰')]/following-sibling::td/text()").extract_first()
        item["linkman"] = "".join(response.xpath("//th[contains(text(),'联系人︰')]/following-sibling::td/text()").extract())
        item["telephone"] = "".join(response.xpath("//th[contains(text(),'电话︰')]/following-sibling::td/text()").extract())
        item["phone"] = "".join(response.xpath("//th[contains(text(),'手机︰')]/following-sibling::td/text()").extract())
        item["E_Mail"] = "".join(response.xpath("//th[contains(text(),'公司邮箱︰')]/following-sibling::td/text()").extract())
        item["contact_Fax"] = response.xpath("//th[contains(text(),'传真︰')]/following-sibling::td/text()").extract_first()
        item["contact_QQ"] = "".join(response.xpath("//img[@title='点击这里给我发消息']/../@href").extract())
        item["Source"] = response.url

        city_infos = response.xpath("//th[contains(text(),'国家/地区︰')]/following-sibling::td/h3/text()").extract_first()
        if city_infos:
            pattern1 = re.compile(r'(.*?)省(.*?)市',re.S)
            # 广东/潮州市
            # 广东省深圳市
            try:
                item["province"] = re.findall(pattern1,city_infos)[0][0]
                item["city_name"] = re.findall(pattern1,city_infos)[0][1]
            except:
                item["province"] = ''
                item["city_name"] = ''
        else:
            item["province"] = ''
            item["city_name"] = ''

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|（个人账号）', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace(' ', '|').replace('-', '|')\
                .replace('、', '|').replace('，', '|').replace('，', '|').replace('.', '').strip()
        else:
            item["kind"] = ''

        item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

        if item["linkman"]:
            item["linkman"] = item["linkman"]
        else:
            item["linkman"] = ''
        item["linkman"] = self.cw.search_linkman(item["linkman"])

        if item["phone"]:
            item["phone"] = item["phone"]
        else:
            item["phone"] = ''
        item["phone"] = self.cw.search_phone_num(item["phone"])

        if item["telephone"]:
            item["telephone"] = item["telephone"]
        else:
            item["telephone"] = ''
        item["telephone"] = self.cw.search_telephone_num(item["telephone"])

        if item["contact_Fax"]:
            item["contact_Fax"] = item["contact_Fax"]
        else:
            item["contact_Fax"] = ''
        item["contact_Fax"] = self.cw.search_contact_Fax(item["contact_Fax"])

        if item["contact_QQ"]:
            item["contact_QQ"] = "".join(re.findall(pattern,item["contact_QQ"])) if re.findall(pattern,item["contact_QQ"]) else ''
        else:
            item["contact_QQ"] = ''
        item["contact_QQ"] = self.cw.search_QQ(item["contact_QQ"])

        if item["E_Mail"]:
            item["E_Mail"] = self.cw.search_email(item["E_Mail"])
        else:
            item["E_Mail"] = (item["contact_QQ"] + "@qq.com") if item["contact_QQ"] else ''

        if item["company_address"]:
            item["company_address"] = item["company_address"].replace(",","").replace('，', '|').strip()
        else:
            item["company_address"] = ''
        item["company_address"] = self.cw.search_address(item["company_address"])

        # if item["host_href"]:
        #     item["host_href"] = item["host_href"]
        # else:
        #     item["host_href"] = ''

        yield item

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''


if __name__ == '__main__':
    execute(["scrapy", "crawl", "diytrade"])