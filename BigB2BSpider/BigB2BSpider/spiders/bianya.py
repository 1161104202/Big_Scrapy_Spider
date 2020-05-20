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
from BigB2BSpider.items import BianYaQiChangYeWangItem
# from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.cmdline import execute



class BianYaQiChangYeWangSpider(CrawlSpider):
    name = "bianya"
    allowed_domains = ['www.bianya.org']
    start_urls = ['http://www.bianya.org/yp.htm']
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
            allow=r".*",restrict_xpaths=("//div[@id='yp_footr_fenlei']//ul//li//a")),follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=(
                "//div[@id='liebiao']//li[@id='clear']//div[@class='button']//a[2]")), callback='parse_items', follow=True),

        Rule(LinkExtractor(
            allow=r".*", restrict_xpaths=("//div[@class='page']//a[contains(text(),'下一页')]")), follow=True),
    )

    def parse_items(self, response):
        item = BianYaQiChangYeWangItem()
        pattern_cm = re.compile('<title>(.*?)-变压器产业网</title>')
        pattern_c = re.compile(r'<br>版权所有： (.*?)&nbsp;&nbsp;&nbsp;&nbsp;Powered By <',re.S)
        pattern_k = re.compile(r'>◆&nbsp;主营行业： (.*?)<',re.S)
        pattern_kd = re.compile(r'>◆&nbsp;主营业务： (.*?) <', re.S)
        pattern_l = re.compile(r'>◆&nbsp;联系人： (.*?)<', re.S)
        pattern_tp = re.compile(r'>◆&nbsp;电  话： (.*?)<', re.S)
        pattern_f = re.compile(r'>◆&nbsp;传  真： (.*?)<', re.S)
        pattern_p = re.compile(r'>◆&nbsp;手  机： (.*?)<',re.S)
        pattern_e = re.compile(r">◆&nbsp;E-mail： <a href='.*?'>(.*?)</a>", re.S)
        pattern_q = re.compile(r'>◆&nbsp;腾讯QQ： <a href=".*?" target="_blank">(.*?)</a>', re.S)
        pattern_add = re.compile(r'>◆&nbsp;详细地址： (.*?)<', re.S)
        pattern_i = re.compile(r'>◆&nbsp;省 市 区： (.*?) / (.*?)<',re.S)
        if response.text:
            try:
                item["company_Name"] = "".join(re.findall(pattern_c,response.text)) if re.findall(pattern_c,response.text) else ''
                item["kind"] = "".join(re.findall(pattern_k,response.text)) if re.findall(pattern_k,response.text) else "".join(re.findall(pattern_kd,response.text))
                item["linkman"] = "".join(re.findall(pattern_l,response.text)) if re.findall(pattern_l,response.text) else ''
                item["phone"] = "".join(re.findall(pattern_p,response.text)) if re.findall(pattern_p,response.text) else ''
                item["telephone"] = "".join(re.findall(pattern_tp,response.text)) if re.findall(pattern_tp,response.text) else ''
                item["contact_Fax"] = "".join(re.findall(pattern_f,response.text)) if re.findall(pattern_f,response.text) else ''
                item["E_Mail"] = "".join(re.findall(pattern_e,response.text)) if re.findall(pattern_e,response.text) else ''
                item["contact_QQ"] = "".join(re.findall(pattern_q,response.text)) if re.findall(pattern_q,response.text) else ''
                item["company_address"] = "".join(re.findall(pattern_add,response.text)) if re.findall(pattern_add,response.text) else ''
                item["province"] = "".join(re.findall(pattern_i,response.text)[0][0]) if re.findall(pattern_i,response.text) else ''
                item["city_name"] = "".join(re.findall(pattern_i,response.text)[0][1]) if re.findall(pattern_i,response.text) else ''
                item["Source"] = response.url
            except Exception as e:
                print(e)
                pass
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
                    .replace(',','|').replace('、', '|').replace(',', '|').replace('，', '|').replace(';','|').replace('.', '').strip()
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
        yield item



        # item["company_Name"] = response.xpath("//td[contains(text(),'公司名称：')]/following-sibling::td/text()").extract_first()
        # item["company_address"] = response.xpath("//td[contains(text(),'公司地址：')]/following-sibling::td/a/text()").extract_first()
        # item["linkman"] = response.xpath("//td[contains(text(),'联 系 人：')]/following-sibling::td/text()").extract_first()
        # item["telephone"] = response.xpath("//td[contains(text(),'公司电话：')]/following-sibling::td/text()").extract_first()
        # item["phone"] = response.xpath("//td[contains(text(),'手机号码：')]/following-sibling::td/text()").extract_first()
        # item["contact_Fax"] = response.xpath("//td[contains(text(),'公司传真：')]/following-sibling::td/text()").extract_first()
        # item["contact_QQ"] = response.xpath("//img[@title='点击QQ交谈/留言']/../@href").extract_first()
        # item["E_Mail"] = response.xpath("//td[contains(text(),'电子邮件：')]/following-sibling::td/text()").extract_first()
        # item["Source"] = response.url
        # item["kind"] = ",".join(response.xpath("//div[@class='head']//h4/text()").getall())
        # city_infos = response.xpath("//dt[contains(text(),'所在地区：')]/following-sibling::dd/text()").get()

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
    execute(["scrapy", "crawl", "bianya"])