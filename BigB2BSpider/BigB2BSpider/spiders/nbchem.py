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
from BigB2BSpider.items import ZhongGuoHuaDongHuaGongWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ZhongGuoHuaDongHuaGongWangSpider(CrawlSpider):
    name = "nbchem"
    allowed_domains = ['www.nbchem.com','nbchem.com']
    start_urls = ['http://www.nbchem.com']
    cw = CleanWords()
    page_count = 0
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
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
        a_list = response.xpath("//div[@id='p2']//table[@align='center']//td[@valign='top']//div//a")
        for a in a_list:
            kind_name = a.xpath("./text()").get()
            kind_href = a.xpath("./@href").get()
            if kind_href:
                kind_href = "http://www.nbchem.com" + kind_href
                # print(kind_name,kind_href)
                # list2-306.html
                kind_num = kind_href.split("list2-")[-1].split(".html")[0]
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    meta={"info":kind_num},
                    dont_filter=True
                )

    def parse_company_list(self, response):
        if "没有公司" in response.text:
            return

        pattern = re.compile(r'</span>\)主要产品：(.*?)\s*</div>',re.S)
        kinds = re.findall(pattern,response.text) if re.findall(pattern,response.text) else ''
        td_list = response.xpath("//div[@class='page']//table[3]//td[@valign='top']//div//table[@width='100%']//td")
        for td in td_list:
            item = ZhongGuoHuaDongHuaGongWangItem()
            item["kind"] = "".join(td.xpath(".//div[2]//text()").getall()).strip()
            contact_href = td.xpath(".//div[4]/a/@href").get()
            if contact_href and "dtcon-" in contact_href:
                # http://www.nbchem.com/bc/dtcon-15691.html
                contact_href = "http://www.nbchem.com/bc/" + contact_href
                # print(contact_href)
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )
        kind_num = response.meta.get("info")
        if kind_num:
            total_page = response.xpath("//div[@class='nbchem']//span[@id='ctl00_ContentPlaceHolder1_PageNav1_labPage']/text()").get()
            if total_page:
                total_page_num = total_page.split('/')[-1]
                if self.page_count < int(total_page_num):
                    self.page_count += 1
                    next_page_url = "http://www.nbchem.com/bc/list2-{}-0-0-0-{}.html".format(kind_num,self.page_count)
                    print(next_page_url)
                    # http://www.nbchem.com/bc/list2-435-0-0-0-1.html
                    yield scrapy.Request(
                        url=next_page_url,
                        callback=self.parse_company_list
                    )


    def parse_company_contact(self, response):
        item = response.meta["item"]
        if "contact.aspx" in response.url:
            item["company_Name"] = response.xpath(
                "//td[contains(text(),'公司名称：')]/following-sibling::td/strong/text()").extract_first()
            item["company_address"] = response.xpath(
                "//td[contains(text(),'地址：')]/following-sibling::td/text()").extract_first()
            item["linkman"] = response.xpath(
                "//td[contains(text(),'联系人：')]/following-sibling::td/text()").extract_first()
            item["telephone"] = response.xpath(
                "//td[contains(text(),'电话：')]/following-sibling::td/text()").extract_first()
            item["phone"] = response.xpath(
                "//td[contains(text(),'手机：')]/following-sibling::td/text()").extract_first()
            item["contact_Fax"] = response.xpath(
                "//td[contains(text(),'传真：')]/following-sibling::td/text()").extract_first()
            item["contact_QQ"] = response.xpath(
                "//td[contains(text(),'QQ：')]/following-sibling::td/a/text()").extract_first()
            item["E_Mail"] = response.xpath(
                "//td[contains(text(),'Email：')]/following-sibling::td/a/text()").extract_first()
            item["Source"] = response.url
            item["kind"] = item["kind"]
            city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()

            if item["company_Name"] and item["company_Name"] != '':
                if "（" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('（')[0]
                elif "(" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('(')[0]
                elif "_" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('_')[0]
                elif "-" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('-')[0]
                else:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ',
                                                                                                          '').strip()
            else:
                return
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            else:
                item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"].replace('未填写', '')
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
                item["company_address"] = self.cw.search_address(item["company_address"])
            else:
                item["company_address"] = ''

            if city_infos:
                if '/' in city_infos:
                    try:
                        item["province"] = city_infos.split('/')[0]
                        item["city_name"] = city_infos.split('/')[1]
                    except:
                        item["province"] = ''
                        item["city_name"] = ''
                else:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''

        else:
            pattern = re.compile(r'<meta name="keywords" content=".*?,(.*?)"/>',re.S)
            item["company_Name"] = response.xpath("//div[@class='ptitle']/span/text()").extract_first()
            item["company_address"] = response.xpath("//td[contains(text(),'地　　址：')]/following-sibling::td/span/text()").extract_first()
            item["linkman"] = response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/span/text()").extract_first()
            item["telephone"] = response.xpath("//td[contains(text(),'电　　话：')]/following-sibling::td/span/text()").extract_first()
            item["phone"] = response.xpath("//td[contains(text(),'移动电话：')]/following-sibling::td/span/text()").extract_first()
            item["contact_Fax"] = response.xpath("//td[contains(text(),'传　　真：')]/following-sibling::td/span/text()").extract_first()
            item["contact_QQ"] = response.xpath("//td[contains(text(),'QQ：')]/following-sibling::td/span/text()").extract_first()
            item["E_Mail"] = response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/span/text()").extract_first()
            item["Source"] = response.url
            item["kind"] = item["kind"]
            city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()


            if item["company_Name"] and item["company_Name"] != '':
                if "（" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('（')[0]
                elif "(" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('(')[0]
                elif "_" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('_')[0]
                elif "-" in item["company_Name"]:
                    item["company_Name"] = item["company_Name"].split('-')[0]
                else:
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
            else:
                return
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
            else:
                item["kind"] = ''

            item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

            if item["linkman"]:
                item["linkman"] = item["linkman"].replace('未填写','')
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
                item["company_address"] = self.cw.search_address(item["company_address"])
            else:
                item["company_address"] = ''

            if city_infos:
                if '/' in city_infos:
                    try:
                        item["province"] = city_infos.split('/')[0]
                        item["city_name"] = city_infos.split('/')[1]
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
    execute(["scrapy", "crawl", "nbchem"])