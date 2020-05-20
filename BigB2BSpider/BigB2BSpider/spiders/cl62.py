# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from hashlib import md5
from scrapy.spiders import CrawlSpider, Rule
from BigB2BSpider.data_tools.clean_worlds import CleanWords
from BigB2BSpider.items import LiuErCaiLiaoWangspiderItem
from BigB2BSpider.data_tools.orc_img import recognition_image
from scrapy.cmdline import execute



class LiuErCaiLiaoWangSpider(CrawlSpider):
    name = 'cl62'
    allowed_domains = ['62cl.com','www.62cl.com']
    start_urls = ['http://www.62cl.com/company/']
    cw = CleanWords()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'DEFAULT_REQUEST_HEADERS': {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            # "Cookie":"Hm_lvt_39b391b010992cf89654d83467db5db7=1564969344; Hm_lpvt_39b391b010992cf89654d83467db5db7=1564970833",
            # "Host":"www.mfqyw.com",
            # "Referer":"http://www.mfqyw.com/",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 544,
            # 'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
        },
        'EXTENSIONS': {
        # 'scrapy.extensions.telnet.TelnetConsole': 300,
        'BigB2BSpider.extensions.closespider.CloseSpider': 300,
    }

    }

    def parse(self, response):
        a_list = response.xpath("//div[@class='m']//div[@class='left_26']//div[@class='catalog']//td//a")[0:1]
        for a in a_list:
            kind_name = a.xpath("./text()").extract_first()
            kind_href = a.xpath("./@href").extract_first()
            if kind_name is None:
                kind_name = a.xpath("./strong/text()").extract_first()
            if kind_href:
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        tr_list = response.xpath("//div[@class='left_26']//div[@class='list']//table//tr")[0:1]
        for tr in tr_list:
            item = LiuErCaiLiaoWangspiderItem()
            pattern = re.compile(r'\[(.*?)\/(.*?)\]', re.S)
            item["company_Name"] = tr.xpath(".//li//a/strong/text()").extract_first()
            company_href = tr.xpath(".//li//a/@href").extract_first()
            item["kind"] = tr.xpath(".//li[contains(text(),'主营：')]/text()").extract_first()
            # city_infos = tr.xpath(".//td[@class='f_orange']/text()").extract_first()
            # if city_infos:
            #     # 广东/潮州市
            #     try:
            #         item["province"] = re.findall(pattern, city_infos)[0][0]
            #         item["city_name"] = re.findall(pattern, city_infos)[0][1]
            #     except:
            #         item["province"] = ''
            #         item["city_name"] = ''
            # else:
            item["province"] = ''
            item["city_name"] = ''
            if company_href:
                # print(company_href)
                contact_href = company_href + "contact/"
                yield scrapy.Request(
                    url=contact_href,
                    callback=self.parse_company_contact,
                    meta={"item": item},
                    dont_filter=True
                )

        # next_page_url = response.xpath("//div[@class='pages']//a[contains(text(),'下一页»')]").extract_first()
        # if next_page_url:
        #     yield scrapy.Request(
        #         url=next_page_url,
        #         callback=self.parse_company_list,
        #         dont_filter=True
        #     )

    def parse_company_contact(self, response):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "BAIDU_SSP_lcr=https://www.baidu.com/link?url=EgzqEOOIMaCoVW2WYHJmZqKJwkuFSCL-ix6-CSiw-HG&wd=&eqid=d504a861000123e5000000065d522b86; bdshare_firstime=1565666217352; Hm_lvt_c7894de9c1e0658a1d1ab0f838038a41=1565666506; UM_distinctid=16c88fef598502-0be4cc78daa5a1-5a13331d-1fa400-16c88fef5994a5; CNZZDATA4515303=cnzz_eid%3D441980283-1565665335-http%253A%252F%252Fwww.jzqncy.com%252F%26ntime%3D1565665335; Hm_lpvt_c7894de9c1e0658a1d1ab0f838038a41=1565666514",
            # "Host": "www.jzqncy.com",
            "Referer": response.url,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }

        item = response.meta["item"]
        item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        item["company_address"] = response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/text()").extract_first()
        item["linkman"] = response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract_first()
        item["telephone"] = response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/img/@src").extract_first()
        item["phone"] = response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/img/@src").extract_first()
        item["contact_Fax"] = response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/img/@src").extract_first()
        item["contact_QQ"] = response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract_first()
        item["E_Mail"] = response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/img/@src").extract_first()
        item["Source"] = response.url

        if item["company_Name"]:
            item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：', '', item["company_Name"]).replace(' ', '').strip()
        item["company_id"] = self.get_md5(item["company_Name"])

        if item["kind"]:
            item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营', '', item["kind"]).replace('-', '|').replace('、', '|') \
                .replace('，', '|').replace('，', '|').replace('.', '').strip()
        else:
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
        res = requests.get(url=url, headers=headers, timeout=20, verify=False)
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
    execute(["scrapy", "crawl", "cl62"])