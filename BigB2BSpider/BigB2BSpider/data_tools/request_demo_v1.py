# -*- coding: utf-8 -*-
# from requests_html import HTMLSession
# session = HTMLSession()
#
# res = session.get('https://news.hao123.com/wangzhi')
# # print(res.text)
#
# # # 获取页面上的所有链接。
# # all_links =  res.html.links
# # print(all_links)
# #
# # # 获取页面上的所有链接，以绝对路径的方式。
# # all_absolute_links = res.html.absolute_links
# # print(all_absolute_links)
#
# links_list = []
# news = res.html.find("#bd > div:nth-child(1)")
# for n in news:
#     # print(n.text)
#     # print(n.absolute_links)
#     # print(n.html)
#     new_link = n.links
#     links_list.append(new_link)
# # print(links_list)
# # print(len(links_list))
# for i in links_list:
#     print(i)
import os,sys
import requests
from lxml import etree


class DocSpider(object):
    def __init__(self):
        self.path = os.path.abspath(sys.argv[0])
        self.base_url = "http://www.mju.edu.cn/tzgg/list.htm"
        # self.doc_url = "http://www.mju.edu.cn/_upload/article/files/44/aa/bdbed40246938f89118335a7b39d/e974ad39-2a8f-41d7-a05c-cf45cc057e79.doc"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "www.mju.edu.cn",
            # "Referer": "http://www.mju.edu.cn/tzgg/list.htm",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
        }

    def parse_base_html(self):
        res = requests.get(url=self.base_url,headers=self.headers,timeout=10,verify=False)
        if res.status_code == 200:
            res.encoding = "utf-8"
            doc_text = res.text
            html = etree.HTML(doc_text)
            li_list = html.xpath("//div[@class='list_main_content']/ul//li")
            if len(li_list) > 0:
                info_list = []
                for li in li_list:
                    item = {}
                    pub_time = "".join(li.xpath("./span[@class='list_time']/text()"))
                    title = "".join(li.xpath(".//span[@class='list_title']/a/@title"))
                    href = "".join(li.xpath(".//span[@class='list_title']/a/@href"))
                    if href:
                        href = "http://www.mju.edu.cn" + href
                    if pub_time:
                        item['pub_time'] = pub_time
                    if title:
                        item['title'] = title
                    if href:
                        item['href'] = href
                    info_list.append(item)
                return info_list
                # print(pub_time,title,href)

    def parse_doc_html(self,info_list):
        if info_list:
            doc_urls_list = []
            for i in info_list:
                print(i)
                link_href = i.get('href')
                if link_href:
                    res = requests.get(url=link_href,headers=self.headers,timeout=10,verify=False)
                    if res.status_code == 200:
                        res.encoding = "utf-8"
                        if "详见附件。" in res.text:
                            html = etree.HTML(res.text)
                            doc_href = "".join(html.xpath("//p[contains(text(),'详见附件。')]"
                                                          "/following-sibling::p//a/@href"))
                            if doc_href:
                                doc_href = "http://www.mju.edu.cn" + doc_href
                                print(doc_href)
                                doc_urls_list.append(doc_href)
            return doc_urls_list

    def parse_html(self,doc_urls_list):
        if doc_urls_list:
            for d in doc_urls_list:
                print(d)
                res = requests.get(url=d, headers=self.headers, timeout=10, verify=False)
                doc_content = res.content
                file_name = d.split('/')[-1]
                if os.path.isfile(file_name):
                    print("文件已经存在")
                    pass
                else:
                    with open(file_name,'wb') as fp:
                        fp.write(doc_content)
                        print("文件获取成功")
                    fp.close()

    def run(self):
        info_list = self.parse_base_html()
        doc_urls_list = self.parse_doc_html(info_list)
        self.parse_html(doc_urls_list)

if __name__ == '__main__':
    ds = DocSpider()
    ds.run()



