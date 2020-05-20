import re
import jieba.analyse



class CleanWords(object):
    def __init__(self):
        pass
    # 处理行业关键字
    def rinse_keywords(self, value):
        result_list = []
        for i in value.split('|'):
            result_list.append(
                ''.join(jieba.analyse.extract_tags(i, topK=5, withWeight=False)))
        result = '|'.join(set([i for i in result_list if i]))
        if result:
            return result
        else:
            return ''

    # replace 方法
    def replace_ss(self, text, args=''):
        if text:
            args = list(args) + ['\r', '\n', ' ', '\t', '\xa0', '\u3000']
            for i in args:
                text = text.replace(i, '')
            return text
        return ''

    # 清洗手机
    def search_phone_num(self, text):
        if text:
            try:
                pattern = re.compile(r'1[35678]\d{9}', re.S)
                text = re.sub(r'\s|\r|\t|\n|保密|移动电话：|电话：|未填写|<|手机：|联系方式：', '', text).strip()
                # text = re.search(r'1\d{10}',text).group(0)
                text = "".join(re.findall(pattern, text)[0])
                return text
            except:
                return ''
        else:
            return ''

    # 清洗电话号码
    def search_telephone_num(self, text):
        if text:
            try:
                pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
                text = re.sub(r'\s|\r|\t|\n|公司电话：|：|暂未提供|未填写|电话：|联系方式：', '', text).strip()
                text = "".join(re.findall(pattern, text)[0])
                return text
            except:
                return ''
        else:
            return ''

    # 清洗传真号码
    def search_contact_Fax(self, text):
        if text:
            try:
                pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
                # '公司联系人：胡'
                text = re.sub(r'\s|\r|\t|\n|公司传真：|：|暂未提供|未填写|暂无|没填', '', text).strip()
                text = "".join(re.findall(pattern, text)[0])
                return text
            except:
                return ''
        else:
            return ''

    # 清洗url
    def search_url(self, text):
        if text:
            try:
                pattern = re.compile(
                    r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|"
                    r"([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)", re.S)
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''

        else:
            return ''

    # 清洗email
    def search_email(self, text):
        if text:
            try:
                pattern = re.compile(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", re.S)
                text = re.sub(r'\s|\r|\t|\n|邮箱：|：|暂未提供|无|暂无', '', text).strip()
                text = "".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ""

    # 清洗QQ
    def search_QQ(self, text):
        if text:
            try:
                pattern = re.compile(r"([1-9]\d{4,10})", re.S)
                text = re.sub(r'\s|\r|\t|\n|QQ：|：|暂未提供|未填写', '', text).strip()
                text = "|".join(re.findall(pattern, text))
                return text
            except:
                return ''
        else:
            return ''

    # 清洗联系人
    def search_linkman(self, text):
        if text:
            try:
                if "：" in text:
                    text = text.split('：')[-1].strip()
                    if len(text) > 3:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士|先生|小姐', '', text)[:3]
                        return text.strip()
                    else:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士', '', text)
                        return text

                elif ":" in text:
                    text = text.split('：')[-1].strip()
                    if len(text) > 3:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士|先生|小姐', '', text)[:3]
                        return text.strip()
                    else:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士', '', text)
                        return text

                elif "(" in text:
                    text = text.split('(')[0].strip()
                    if len(text) > 3:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士|先生|小姐', '', text)[:3]
                        return text.strip()
                    else:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士', '', text)
                        return text

                elif "（" in text:
                    text = text.split('（')[0].strip()
                    if len(text) > 3:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士|先生|小姐', '', text)[:3]
                        return text.strip()
                    text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士', '', text)
                    return text

                elif "&" in text:
                    text = text.split('&')[0].strip()
                    if len(text) > 3:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士|先生|小姐', '', text)[:3]
                        return text.strip()
                    text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士', '', text)
                    return text

                # elif " " in text:
                #     text = text.split(' ')[0].strip()
                #     if len(text) > 3:
                #         text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女|男', '', text)
                #         return text.strip()
                #     else:
                #         text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女|男', '', text)
                #         return text
                elif "、" in text:
                    text = text.split('、')[0].strip()
                    if len(text) > 3:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士|小姐', '', text)[:3]
                        return text.strip()
                    else:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-|·联系人：|女士|男士', '', text)
                        return text
                else:
                    text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-', '', text)
                    if len(text) >3:
                        text = re.sub(r'先生|女士|小姐|未填写|-|女士|男士|小姐','',text)[:3]
                        return text
                    else:
                        text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-', '', text)
                        return text
            except:
                return ''
        else:
            return ''

    # 清洗地址
    def search_address(self, text):
        if text:
            if "：" in text:
                try:
                    text = text.split("：")[-1]
                    if text:
                        # '公司地址：中国  广东  广州  番禺区沙头街嘉品二街二号1栋1529'
                        text = re.sub(r'\s|\r|\n|\t|地址|公司地址|公司地址：|：|暂未提供|未填写|企业地址|·|详细地址：|-', '', text)
                        # pattern = re.compile(r'(www.\w+.\w{2,3})',re.S)
                        # text = re.sub(pattern,'',text)
                        if text:
                            return text
                    else:
                        return ''
                except:
                    return ''
            text = re.sub(r'\s|\r|\n|\t|地址|公司地址|公司地址：|：|暂未提供|未填写|企业地址|·|详细地址：|-', '', text)
            pattern = re.compile(r'(www.\w+.\w{2,3})', re.S)
            text = re.sub(pattern, '', text)
            if text:
                return text
        else:
            return ''

    # 清洗公司
    def search_company(self, text):
        if text and text != '':
            if "：" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split('：')[-1])
                if text:
                    # text = self.get_regex(text)
                    return text
            elif ":" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split(':')[-1])
                if text:
                    # text = self.get_regex(text)
                    return text
            elif text.endswith("）"):
                text = re.sub(r'\s|\n|\r|\t', '', text.split('（')[0])
                if text:
                    # text = self.get_regex(text)
                    return text
            elif text.endswith(")"):
                text = re.sub(r'\s|\n|\r|\t', '', text.split('(')[0])
                if text:
                    # text = self.get_regex(text)
                    return text
            elif "_" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split('_')[0])
                if text:
                    # text = self.get_regex(text)
                    return text
            elif "-" in text:
                text = re.sub(r'\s|\n|\r|\t', '', text.split('-')[0])
                if text:
                    # text = self.get_regex(text)
                    return text
            else:
                text = re.sub(r'\n|\s|\r|\t|公司名称：', '', text).replace(' ', '').strip()
                if text:
                    try:
                        # text = self.get_regex(text)
                        # print(text)
                        return text
                    except:
                        return ''
                else:
                    return text
        else:
            return ''

    def get_regex(self, value):
        result = []
        result_r = []
        pattern_list = [r'(\d+)', r'(www.\w+.\w{2,3})']
        for p in pattern_list:
            res = "".join(re.findall(p, value))
            if res:
                result.append(res)
        if result:
            # print(result)
            try:
                for rs in result:
                    res = ''
                    res = re.sub(rs, '', value)
                    value = res
                    if value:
                        result_r.append(value)
            except:
                return ''
        if result_r:
            return "".join(result_r[-1])
        else:
            return value



if __name__ == '__main__':
    cw = CleanWords()