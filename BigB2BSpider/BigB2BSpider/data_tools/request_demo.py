# # -*- coding: utf-8 -*-
# # from requests_html import HTMLSession
# # session = HTMLSession()
# #
# # res = session.get('https://news.hao123.com/wangzhi')
# # # print(res.text)
# #
# # # # 获取页面上的所有链接。
# # # all_links =  res.html.links
# # # print(all_links)
# # #
# # # # 获取页面上的所有链接，以绝对路径的方式。
# # # all_absolute_links = res.html.absolute_links
# # # print(all_absolute_links)
# #
# # links_list = []
# # news = res.html.find("#bd > div:nth-child(1)")
# # for n in news:
# #     # print(n.text)
# #     # print(n.absolute_links)
# #     # print(n.html)
# #     new_link = n.links
# #     links_list.append(new_link)
# # # print(links_list)
# # # print(len(links_list))
# # for i in links_list:
# #     print(i)
# import os,sys
# import requests
#
#
# class DocSpider(object):
#     def __init__(self):
#         self.path = os.path.abspath(sys.argv[0])
#         self.doc_url = "http://www.mju.edu.cn/_upload/article/files/44/aa/bdbed40246938f89118335a7b39d/e974ad39-2a8f-41d7-a05c-cf45cc057e79.doc"
#         self.headers = {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#             "Accept-Encoding": "gzip, deflate",
#             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
#             "Cache-Control": "max-age=0",
#             "Connection": "keep-alive",
#             "Host": "www.mju.edu.cn",
#             "Referer": "http://www.mju.edu.cn/tzgg/list.htm",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
#         }
#
#     def parse_html(self):
#         res = requests.get(url=self.doc_url,headers=self.headers,timeout=10,verify=False)
#         if res.status_code == 200:
#             res.encoding = "utf-8"
#             doc_content = res.content
#             # print(doc_content)
#             # print(res.content)
#             file_name = self.doc_url.split('/')[-1]
#             if os.path.isfile(file_name):
#                 print("文件已经存在")
#                 pass
#             else:
#                 with open(file_name,'wb') as fp:
#                     fp.write(doc_content)
#                     print("文件写入成功")
#                 fp.close()
#
#     def run(self):
#         self.parse_html()
#
# if __name__ == '__main__':
#     ds = DocSpider()
#     ds.run()


# import re
# regex = re.compile(r"[\u4e00-\u9fa5]")
# results = "".join(re.findall(regex,"智能家居 \0x4576b6\d8"))
# print(results)

import re

# pattern_p = r'([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市)){0,1}([\u4e00-\u9fa5]{2,7}?(?:区|县|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:村|镇|街道)){1}'
# regex = r'([\u4e00-\u9fa5]{2,5})[省]|([\u4e00-\u9fa5]{2,5})[市]'

# pattern_p = re.compile(r'([\u4e00-\u9fa5]{2,5})省',re.S)
# pattern_c = re.compile(r'[省]([\u4e00-\u9fa5]{2,5})市',re.S)
#
# str = "深圳市宝安区沙井镇沙井路1号2栋"
#
# res = re.findall(pattern_c,str)
# print(res)

class CleanWords(object):
    def __init__(self):
        # self.company = "微软科技有限公司www.soft.com67870我是"
        pass
    def search_company(self,text):
        if text and text != '':
            if "：" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split('：')[-1])
                if text:
                    text = self.get_regex(text)
                    return text
            elif ":" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split(':')[-1])
                if text:
                    text = self.get_regex(text)
                    return text
            elif text.endswith("）"):
                text = re.sub(r'\s|\n|\r|\t', '', text.split('（')[0])
                if text:
                    text = self.get_regex(text)
                    return text
            elif text.endswith(")"):
                text = re.sub(r'\s|\n|\r|\t', '', text.split('(')[0])
                if text:
                    text = self.get_regex(text)
                    return text
            elif "_" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split('_')[0])
                if text:
                    text = self.get_regex(text)
                    return text
            elif "-" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split('-')[0])
                if text:
                    text = self.get_regex(text)
                    return text
            else:
                text = re.sub(r'\n|\s|\r|\t|公司名称：', '', text).replace(' ', '').strip()
                if text:
                    text = self.get_regex(text)
                    print(text)
                    return text
        else:
            return ''


    def get_regex(self, value):
        result = []
        result_r = []
        pattern_list = ['(\d+)', r'(www.\w+.\w{2,3})']
        for p in pattern_list:
            res = "".join(re.findall(p, value))
            if res:
                result.append(res)
        if result:
            # print(result)
            try:
                for rs in result:
                    res = ''
                    res = re.sub(rs,'', value)
                    value = res
                    if value:
                        result_r.append(value)
            except:
                return ''
        if result_r:
            return "".join(result_r[-1])
        else:
            return ''


    # def run(self):
    #     text = self.get_regex(self.company)
    #     print(self.search_company(text))

if __name__ == '__main__':
    cl = CleanWords()
    company = "微软科技有限公司我是"
    cl.search_company(company)
    # print(cl.get_regex(company))