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
from BigB2BSpider.items import HuaGongYiQiWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class HuaGongYiQiWangSpider(CrawlSpider):
    name = "chem17"
    allowed_domains = ['www.chem17.com','hem17.com']
    start_urls = ['http://www.chem17.com/company/a_t0/list.html']
    cw = CleanWords()
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

    rules = (
        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//div[@class='companyList']//div[@class='companyName']//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='page']//a[@title='下一页']")), follow=True),

        Rule(LinkExtractor(
            allow=r".*",restrict_xpaths=("//a[contains(text(),'联系我们')]")), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        item = HuaGongYiQiWangItem()
        if "contactus.html" in response.url:
            if response.xpath("//article[@class='rightContent']//h2/text()").get() is not None:
                pattern20 = re.compile(r'<b>.*?主营产品：(.*?)</b>',re.S)
                item["company_Name"] = response.xpath("//div[@class='contactUs']/strong/text()").get()
                item["company_address"] = response.xpath("//div[@class='contactUs']//p[contains(text(),'详细地址：')]/text()").get()
                item["linkman"] = response.xpath("//div[@class='contactUs']//p[contains(text(),'联 系 人  ：  ')]/i/text()").get()
                item["telephone"] = "".join(response.xpath("//div[@class='contactUs']//p[contains(text(),'电')]//text()").getall())
                item["phone"] = "".join(response.xpath("//div[@class='contactUs']//p[contains(text(),'手')]//text()").getall())
                item["contact_Fax"] = "".join(response.xpath("//div[@class='contactUs']//p[contains(text(),'传')]//text()").getall())
                item["contact_QQ"] = response.xpath("//b[contains(text(),'在线交流')]/../@href").get()
                item["E_Mail"] = response.xpath("//div[@class='contactUs']//p[contains(text(),'详细地址：')]/text()").get()
                item["Source"] = response.url
                item["kind"] = response.xpath("//div[@class='foot']/p/text()").get()
                # city_infos = response.xpath("//div[@class='contactUs']//p[contains(text(),'详细地址：')]/text()").get()

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
                        item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|联系我们－', '', item["company_Name"])\
                            .replace(' ','').strip()
                else:
                    return
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    try:
                        item["kind"] = item["kind"].split("： ")[-1].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"])\
                            .replace('-', '|').replace('、', '|').replace(',', '|').replace('，', '|')\
                            .replace(';', '|').replace('.','').strip()
                    except:
                        item["kind"] = ''
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
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
                item["province"] = ''
                item["city_name"] = ''
                yield item

            elif "联系方式" in "".join(response.xpath("//i[@class='line']/following-sibling::h2//text()").getall()):
                pattern50 = re.compile(r'<TITLE>联系我们－(.*?)</TITLE>', re.S)
                pattern30 = re.compile(r'>E-Mail：(.*?)<', re.S)
                pattern31 = re.compile(r'<span>公司名称：</span>(.*?)<br>', re.S)
                pattern1 = re.compile(r'<span>联系人：</span>(.*?)<br>', re.S)
                pattern2 = re.compile(r' <span>详细地址：</span> (.*?)<br>', re.S)
                pattern3 = re.compile(r'<span>电话号码：</span> (.*?)<br>', re.S)
                pattern4 = re.compile(r'<span>手机号码：</span>(.*?)<br>', re.S)
                pattern5 = re.compile(r'<span>传真号码：</span>  (.*?)<br>', re.S)
                pattern6 = re.compile(r'>电子邮件：(.*?)<', re.S)
                pattern7 = re.compile(r'<em>QQ：</em>(.*?)<br />', re.S)
                pattern8 = re.compile(r'<li>所在地区：(.*?)</li>', re.S)
                pattern9 = re.compile(r'>主营：(.*?)<', re.S)
                pattern10 = re.compile(r'</h1>\s*<p>(.*?)</p>\s*</div>',re.S)
                item["company_Name"] = "".join(re.findall(pattern50,response.text)) if re.findall(pattern50,response.text) else ''
                item["company_address"] = "".join(re.findall(pattern2,response.text)) if re.findall(pattern2,response.text) else ''
                item["linkman"] = "".join(re.findall(pattern1,response.text)) if re.findall(pattern1,response.text) else ''
                item["telephone"] = "".join(re.findall(pattern3,response.text)) if re.findall(pattern3,response.text) else ''
                item["phone"] = "".join(re.findall(pattern4,response.text)) if re.findall(pattern4,response.text) else ''
                item["contact_Fax"] = "".join(re.findall(pattern5,response.text)) if re.findall(pattern5,response.text) else ''
                item["contact_QQ"] = response.xpath("//b[contains(text(),'在线交流')]/../@href").get()
                item["E_Mail"] = "".join(re.findall(pattern30, response.text)[0]) if re.findall(pattern30,response.text) else ''
                item["Source"] = response.url
                item["kind"] = response.xpath("//h3[contains(text(),'主营产品')]/following-sibling::p/text()").get()
                # city_infos = ",".join(re.findall(pattern8, response.text)) if re.findall(pattern8, response.text) else ''

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
                        item["company_Name"] = re.sub(
                            r'\n|\s|\r|\t|公司名称：|联系我们－', '', item["company_Name"]).replace(' ','').strip()
                else:
                    return
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    try:
                        item["kind"] = item["kind"].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"])\
                            .replace('-', '|').replace('、', '|').replace(',', '|').replace('，', '|')\
                            .replace(';', '|').replace('.','').strip()
                    except:
                        item["kind"] = ''
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
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

                item["province"] = ''
                item["city_name"] = ''

                yield item


            else:
                pattern = re.compile(r'<TITLE>联系我们－(.*?)</TITLE>', re.S)
                pattern30 = re.compile(r'>E-Mail：(.*?)<',re.S)
                pattern60 = re.compile(r'<p>.*? - 主营产品：(.*?)</p>',re.S)
                # pattern1 = re.compile(r'联系人：(.*?)<', re.S)
                # pattern2 = re.compile(r'地址：(.*?)<', re.S)
                # pattern3 = re.compile(r'电话：(.*?)<', re.S)
                # # >手机：13920418181<
                # pattern4 = re.compile(r'>手机：(.*?)<', re.S)
                # pattern5 = re.compile(r'>传真：(.*?)<', re.S)
                # pattern6 = re.compile(r'>电子邮件：(.*?)<', re.S)
                # pattern7 = re.compile(r'<em>QQ：</em>(.*?)<br />', re.S)
                # pattern8 = re.compile(r'<li>所在地区：(.*?)</li>', re.S)
                # pattern9 = re.compile(r'>主营：(.*?)<', re.S)
                # pattern10 = re.compile(r'</h1>\s*<p>(.*?)</p>\s*</div>',re.S)
                item["company_Name"] = response.xpath("//div[@class='contact-company']/table//td[@valign='middle']/text()").get()
                item["company_address"] = response.xpath("//dt[contains(text(),'详细地址：')]/..//dd/text()").get()
                item["linkman"] = "".join(response.xpath("//div[@class='contact-person']//text()").getall()).strip()
                item["telephone"] = response.xpath("//div[@class='contact-more']//dt[contains(text(),'电')]/..//dd/text()").get()
                item["phone"] = response.xpath("//div[@class='contact-more']//dt[contains(text(),'手')]/..//dd/text()").get()
                item["contact_Fax"] = response.xpath("//div[@class='contact-more']//dt[contains(text(),'传')]/..//dd/text()").get()
                item["contact_QQ"] = response.xpath("//b[contains(text(),'在线交流')]/../@href").get()
                item["E_Mail"] = "".join(re.findall(pattern30, response.text)[0]) if re.findall(pattern30, response.text) else ''
                item["Source"] = response.url
                item["kind"] = response.xpath("//div[@id='bottom']/b/text()").get()
                # city_infos = ",".join(re.findall(pattern8, response.text)) if re.findall(pattern8, response.text) else ''


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
                        item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|联系我们－', '', item["company_Name"]).replace(' ', '').strip()
                else:
                    return
                item["company_id"] = self.get_md5(item["company_Name"])

                if item["kind"]:
                    try:
                        item["kind"] = item["kind"].split("：")[-1].replace(" ", '|')
                        item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|')\
                            .replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
                    except:
                        item["kind"] = ''
                else:
                    item["kind"] = ''

                item["kind"] = self.cw.rinse_keywords(self.cw.replace_ss(item["kind"]))

                if item["linkman"]:
                    item["linkman"] = item["linkman"]
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

                item["province"] = ''
                item["city_name"] = ''

                yield item
        else:
            pattern11 = re.compile(r'<TITLE>(.*?)</TITLE>', re.S)
            pattern12 = re.compile(r'<th>联系人</th>\s*<td>(.*?)</td>',re.S)
            pattern13 = re.compile(r'<th>联系电话</th>\s*<td>(.*?)</td>', re.S)
            pattern14 = re.compile(r'<th>手机</th>\s*<td>(.*?)</td>', re.S)
            pattern15 = re.compile(r'<th>联系传真</th>\s*<td>(.*?)</td>', re.S)
            pattern16 = re.compile(r'<th>联系地址</th>\s*<td>(.*?)</td>', re.S)
            pattern17 = re.compile(r'<th>联系邮箱</th>\s*<td>(.*?)</td>', re.S)
            pattern18 = re.compile(r'>主营：(.*?)<', re.S)
            pattern19 = re.compile(r'<div class="introduce_content"><p>(.*?)</p>\s*</div>',re.S)

            item["company_Name"] = "".join(
                re.findall(pattern11, response.text)[0]) if re.findall(pattern11, response.text) else ''
            item["company_address"] = "".join(
                re.findall(pattern16, response.text)[0]) if re.findall(pattern16, response.text) else ''
            item["linkman"] = "".join(
                re.findall(pattern12, response.text)[0]) if re.findall(pattern12, response.text) else ''
            item["telephone"] = "".join(
                re.findall(pattern13, response.text)[0]) if re.findall(pattern13, response.text) else ''
            item["phone"] = "".join(
                re.findall(pattern14, response.text)[0]) if re.findall(pattern14, response.text) else ''
            item["contact_Fax"] = "".join(
                re.findall(pattern15, response.text)[0]) if re.findall(pattern15, response.text) else ''
            item["contact_QQ"] = response.xpath("//b[contains(text(),'在线交流')]/../@href").get()
            item["E_Mail"] = "".join(
                re.findall(pattern17, response.text)[0]) if re.findall(pattern17, response.text) else ''
            item["Source"] = response.url
            item["kind"] = "".join(re.findall(pattern18, response.text)) if re.findall(pattern18, response.text) else ''
            # city_infos = ",".join(re.findall(pattern8, response.text)) if re.findall(pattern8, response.text) else ''

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
                    item["company_Name"] = re.sub(r'\n|\s|\r|\t|公司名称：|联系我们－', '', item["company_Name"]).replace(' ',
                                                                                                                '').strip()
            else:
                return
            item["company_id"] = self.get_md5(item["company_Name"])

            if item["kind"]:
                item["kind"] = item["kind"].replace(" ", '|')
                item["kind"] = re.sub(r'\n|\s|\r|\t|主营业务：|主营|主营项目：', '', item["kind"]).replace('-', '|') \
                    .replace('、', '|').replace(',', '|').replace('，', '|').replace(';', '|').replace('.', '').strip()
            else:
                try:
                    item["kind"] = ",".join(re.findall(pattern19, response.text)) if re.findall(pattern19,
                                                                                                response.text) else ''
                except:
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
    execute(["scrapy", "crawl", "chem17"])