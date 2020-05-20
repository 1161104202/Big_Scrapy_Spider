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
from BigB2BSpider.items import ZhongGuoHuaGongSheBeiWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class ZhongGuoHuaGongSheBeiWangSpider(CrawlSpider):
    name = "ccen_v1"
    allowed_domains = ['www.ccen.net','ccen.net']
    start_urls = ['http://www.ccen.net/company/']
    cw = CleanWords()
    # redis_key = "ksb:start_urls"

    custom_settings = {
        'DOWNLOAD_DELAY': 0.4,
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
        a_list = response.xpath("//table[@class='martop']//table[@class='ccen_blueborder']//table[@style='margin-bottom:5px']//tr//a")
        for a in a_list:
            kind_name = a.xpath("./text()").get()
            kind_href = a.xpath("./@href").get()
            if kind_href:
                kind_href = "http://www.ccen.net/company/" + kind_href
                # print(kind_name,kind_href)
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_company_list,
                    dont_filter=True
                )

    def parse_company_list(self, response):
        t_list = response.xpath("//table[@style='margin-top:10px; border-bottom:1px solid #CCCCCC; padding:5px;']//td[@valign='top']")
        for t in t_list:
            item = ZhongGuoHuaGongSheBeiWangItem()
            # ',,,联系人：,树伟,电话：,025-57467888,手机：,15806100000,更多联系方式>>,,,'
            pattern = re.compile(r'>联系人：</span>(.*?)				　<',re.S)
            pattern1 = re.compile(r'>电话：</span>(.*?)                　<', re.S)
            pattern2 = re.compile(r'>手机：</span>(.*?)                　<', re.S)
            pattern3 = re.compile(r'>主营：</span>(.*?)</td>',re.S)
            pattern4 = re.compile(r'<a href="(.*?)" target="_blank">更多联系方式\&gt;&gt;</a>',re.S)
            item["company_Name"] = t.xpath(".//table[1]//a[@class='blue f14']/@title").get()
            city_infos = t.xpath(".//table[1]//a[@class='blue f14']/../text()").get()
            linkinfos = "".join(t.xpath(".//table[3]").getall())
            item["kind"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
            item["linkman"] = "".join(re.findall(pattern,linkinfos)) if re.findall(pattern,linkinfos) else ''
            item["telephone"] = "".join(re.findall(pattern1,linkinfos)) if re.findall(pattern1,linkinfos) else ''
            item["phone"] = "".join(re.findall(pattern2, linkinfos)) if re.findall(pattern2, linkinfos) else ''
            if city_infos:
                #  [湖北省-武汉]
                pattern_p = re.compile(r'\[(.*?)-.*?\]',re.S)
                pattern_c = re.compile(r'\[.*?-(.*?)\]',re.S)
                if "[" and "-" and "]" in city_infos:
                    try:
                        item["province"] = "".join(re.findall(pattern_p,city_infos)) if re.findall(pattern_p,city_infos) else ''
                        item["city_name"] = "".join(re.findall(pattern_c,city_infos)) if re.findall(pattern_c,city_infos) else ''
                    except:
                        item["province"] = ''
                        item["city_name"] = ''
                else:
                    item["province"] = ''
                    item["city_name"] = ''
            else:
                item["province"] = ''
                item["city_name"] = ''

            company_href = "".join(re.findall(pattern4,linkinfos)[0]) if re.findall(pattern4,linkinfos) else ''
            if company_href:
                yield scrapy.Request(
                    url=company_href,
                    callback=self.parse_company_detail,
                    meta={"item": item},
                    dont_filter=True
                )
            
        next_page_url = response.xpath("//table[@class='membertable_page'][1]//a[contains(text(),'下一页')]/@href").get()
        if next_page_url:
            next_page_url = "http://www.ccen.net" + next_page_url
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_company_list
            )

    def parse_company_detail(self, response):
        item = response.meta["item"]
        contact_href = response.xpath("//font[contains(text(),'联系我们')]/../../@href").get()
        if  contact_href:
            contact_href = response.url + contact_href
            yield scrapy.Request(
                url=contact_href,
                callback=self.parse_company_contact,
                dont_filter=True
            )
        else:
            pattern_add = re.compile(r'>\s*详细地址：(.*?)<',re.S)
            pattern_em = re.compile(r'>\s*电子邮件：(.*?)<',re.S)
            pattern_fa = re.compile(r'>\s*传真：(.*?)<',re.S)
            pattern_k = re.compile(r'<p>主营产品： (.*?)<br />',re.S)
            item["company_Name"] = item["company_Name"]
            item["company_address"] = "".join(
                re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
            item["linkman"] = item["linkman"]
            item["telephone"] = item["telephone"]
            item["phone"] = item["phone"]
            item["contact_Fax"] = "".join(
                re.findall(pattern_fa,response.text)) if re.findall(pattern_fa,response.text) else ''
            item["contact_QQ"] = response.xpath("//a[contains(@title,'点击QQ图标在线联系')]/@href").extract_first()
            item["E_Mail"] = "".join(
                re.findall(pattern_em,response.text)) if re.findall(pattern_em,response.text) else ''
            item["Source"] = response.url
            item["kind"] = ",".join(re.findall(pattern_k,response.text)) if re.findall(pattern_k,response.text) else ''
            # city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()


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
                try:
                    item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
                except:
                    item["contact_QQ"] = ''

            if item["company_address"]:
                item["company_address"] = self.cw.search_address(item["company_address"])
            else:
                item["company_address"] = ''

            # if city_infos:
            #     if '/' in city_infos:
            #         try:
            #             item["province"] = city_infos.split('/')[0]
            #             item["city_name"] = city_infos.split('/')[1]
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


    def parse_company_contact(self,response):
        item = response.meta["item"]
        # pattern = re.compile(r'<title>(.*?) - .*?</title>',re.S)
        # pattern1 = re.compile(r'<p>主营产品： (.*?)<br />',re.S)
        # pattern2 = re.compile(r'>\s*通信地址：(.*?)\&nbsp;',re.S)
        # pattern3 = re.compile(r';\s*电话：(.*?)\&nbsp;',re.S)
        # pattern4 = re.compile(r';\s*传真：(.*?)\s*<', re.S)
        # pattern5 = re.compile(r'>\s*E-mail：(.*?)\&nbsp;', re.S)
        # pattern6 = re.compile(r'>\s*联系人：(.*?)<br />', re.S)
        pattern_k = re.compile(r'>\s*主营产品： (.*?)<',re.S)
        item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td[2]/text()").get()
        item["company_address"] = response.xpath("//td[contains(text(),'详细地址：')]/following-sibling::td[2]/text()").get()
        item["linkman"] = response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td[2]/text()").get()
        item["telephone"] = response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td[2]/text()").get()
        item["phone"] = response.xpath("//td[contains(text(),'手　　机：')]/following-sibling::td[2]/text()").get()
        item["contact_Fax"] = response.xpath("//td[contains(text(),'传　　真：')]/following-sibling::td[2]/text()").get()
        item["contact_QQ"] = response.xpath("//a[contains(@title,'点击QQ图标在线联系')]/@href").extract_first()
        item["E_Mail"] = response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td[2]/text()").extract_first()
        item["Source"] = response.url
        item["kind"] = ",".join(re.findall(pattern_k,response.text)) if re.findall(pattern_k,response.text) else ''
        # city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()


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
            try:
                item["contact_QQ"] = self.cw.search_QQ(item["E_Mail"])
            except:
                item["contact_QQ"] = ''

        if item["company_address"]:
            item["company_address"] = self.cw.search_address(item["company_address"])
        else:
            item["company_address"] = ''

        # if city_infos:
        #     if '/' in city_infos:
        #         try:
        #             item["province"] = city_infos.split('/')[0]
        #             item["city_name"] = city_infos.split('/')[1]
        #         except:
        #             item["province"] = ''
        #             item["city_name"] = ''
        #     else:
        #         item["province"] = ''
        #         item["city_name"] = ''
        # else:
        item["province"] = item["province"]
        item["city_name"] = item["city_name"]

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
    execute(["scrapy", "crawl", "ccen_v1"])