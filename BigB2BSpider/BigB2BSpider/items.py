# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import jieba.analyse
import scrapy
from hashlib import md5
from scrapy.loader import ItemLoader
from scrapy import Item
from scrapy.loader.processors import TakeFirst, MapCompose, Join
# from BigB2BSpider.data_tools.clean_worlds import CleanWords



class Bigb2BspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params

class HuiShangBaoSpiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params

class QiYe39spiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ShangQuWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_05(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class YiWangTuispiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_05(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class YiSiSispiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params




class FaShangJispiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class JiShangWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class RouDianGongChengspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class AnFangZhanspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params




class ZhongGuoAnFangWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ShangLuWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_08(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params




class ZhongGouShangWuWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_08(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params




class WeiLongShangWuWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_08(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class WuJiuShangWuWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_08(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QiYeHuispiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QiMaoWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QiYeWuLiuspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ChangPinLiuLiuYiLiuspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class WangLuoYiYiSispiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class GuoJiMaoYiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ZhongGuoMaoYiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ShangYiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QiZhangWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class LiuErCaiLiaoWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_14(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ZhongAnShangChengspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ZiZhuMaoYiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params

class KuSoBaspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QuanQiuFangZhiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class QuanQiuTieYiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_19(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class BaFangZiYuanWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class WeiKuYiQiYiBiaoWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_19(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ZhiZaoJiaoYiWangspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_19(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ShangMaoTongspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_23(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class YiWuGouspiderItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_20(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class DongShanWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_20(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class DongFangGongYingShanItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_20(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class  WangShangZhiChuangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_20(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class GouLianZiYuanWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_21(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class MingZhanZaiXianItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_21(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params

class ZhongGuoQiYeLianItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_21(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class CebnDianZiShangWuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_21(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class YiLingLingYiSanWuShangWuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_23(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params

class JianShuWangItem(scrapy.Item):
    title = scrapy.Field()
    diamond = scrapy.Field()
    author = scrapy.Field()
    comments = scrapy.Field()
    like = scrapy.Field()
    money = scrapy.Field()




class ShangWuWangKuItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class TaoJinDiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_23(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ShangNiuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ErWuBaWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QuanQiuHuaMuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_22(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class HuangYeBaBaItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class YiShangWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class hengshangWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class QiShangWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ZaoWaiXinXiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class BengFaShangWuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_26(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class WanYouYinLiShangMaoWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_27(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class WuYiSuoLeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_28(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class WuYouJiaoYiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_28(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class HaiShangWuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_28(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class QiLingWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_30(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ELuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_30(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class MouSiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_30(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class QiYeDaHuangYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_30(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ShangMingLuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class SaiMenWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_08_31(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class BaiChuangHuangYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_03(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class QiDuoWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_03(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class GongQiuXingXiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_03(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class DingDingYiErWuBaWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_04(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ErSanSanGongChangWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_04(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class QinCaiHuangYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_04(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class LvDaoWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_04(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class WuJinShangJiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_04(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class HuaGongYiQiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_05(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ZhongGuoHuaDongHuaGongWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_05(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ZhongGuoHuaGongSheBeiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class YiBiaoZhangLanWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class YiQiYiBiaoJiaoYiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_06(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class AYiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_07(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class LvSeJieNengHuanBaoWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_07(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class XinNengYuanWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class CeKongWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class DongShengDianCiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_09(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class BianYaQiChangYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_10(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class BianPinQiChangYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_10(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class BeiJiXingShangWuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_10(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class ZhongHuaChuangGangQiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_10(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class SuoBiGuangFuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_10(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ZhongGuoDianbQiItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_10(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class BenDiSouWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_11(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class WuBaShiPingWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_11(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ShiPinDaiLiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_11(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class NongZiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_11(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class XiBeiMiaoMuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_11(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class NongYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class TongZhuangQiYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class HuangQiuXieYeWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_12(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params



class DianQiZiDongHuaWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class JiChuangShangWuWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class YiWuBaJiXieWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ShuKongJiChuanShiChangWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class JiChuangMaiMaiWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ZhongGuoJiChuangWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ZhongHuaGongKongWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


class ZhiNengZhiZaoWangItem(scrapy.Item):
    company_Name = scrapy.Field()
    company_id = scrapy.Field()
    kind = scrapy.Field()
    linkman = scrapy.Field()
    phone = scrapy.Field()
    telephone = scrapy.Field()
    E_Mail = scrapy.Field()
    contact_Fax = scrapy.Field()
    contact_QQ = scrapy.Field()
    province = scrapy.Field()
    city_name = scrapy.Field()
    company_address = scrapy.Field()
    Source = scrapy.Field()

    def insert_sql(self):
        # ' ON  DUPLICATE KEY UPDATE '
        sql = """
                INSERT INTO enterprise_product_v1_attached_2019_09_16(
                company_Name,company_id,kind,linkman,phone,telephone,E_Mail,contact_Fax,
                contact_QQ,province,city_name,company_address,Source
                ) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                ON DUPLICATE KEY UPDATE 
                company_Name=VALUES(company_Name),
                company_id=VALUES(company_id),
                kind=VALUES(kind),
                linkman=VALUES(linkman),
                phone=VALUES(phone),
                telephone=VALUES(telephone),
                E_Mail=VALUES(E_Mail),
                contact_Fax=VALUES(contact_Fax),
                contact_QQ=VALUES(contact_QQ),
                province=VALUES(province),
                city_name=VALUES(city_name),
                company_address=VALUES(company_address),
                Source=VALUES(Source)
                """

        params = (
            self['company_Name'], self['company_id'], self['kind'], self['linkman'],
            self['phone'], self['telephone'], self['E_Mail'], self['contact_Fax'],
            self['contact_QQ'], self['province'], self['city_name'], self['company_address'],
            self['Source']
        )

        return sql, params


    # define the fields for your item here like:
    # name = scrapy.Field()
    # 自定义itemloader，默认的输出处理器为取第一个非空元素
    # default_output_processor = TakeFirst()
    #
    # # 清洗公司
    # def search_company(self, text):
    #     if text:
    #         try:
    #             # '公司地址：中国  广东  广州  番禺区沙头街嘉品二街二号1栋1529'
    #             result = re.sub(r'\s|\r|\n|\t', '', text)
    #             return result
    #         except:
    #             return text
    #     else:
    #         return ''
    #
    # # 处理行业关键字
    # def rinse_keywords(self, value):
    #     result_list = []
    #     for i in value.split('|'):
    #         result_list.append(
    #             ''.join(jieba.analyse.extract_tags(i, topK=5, withWeight=False)))
    #     result = '|'.join(set([i for i in result_list if i]))
    #     if result:
    #         return result
    #     else:
    #         return ''
    #
    # # replace 方法
    # def replace_ss(self, text, args=''):
    #     if text:
    #         try:
    #             result = re.sub(r'\n|\s|\r|\t|主营业务：', '', text).replace('、', '|')\
    #                 .replace('，', '|').replace('，', '|').replace('.', '').strip()
    #             args = list(args) + ['\r', '\n', ' ', '\t', '\xa0', '\u3000']
    #             for i in args:
    #                 result = result.replace(i, '')
    #             return result
    #         except:
    #             return ''
    #     return ''
    #
    # # 清洗手机
    # def search_phone_num(self, text):
    #     if text:
    #         try:
    #             pattern = re.compile(r'1[35678]\d{9}', re.S)
    #             text = re.sub(r'\s|\r|\t|\n|保密|移动电话：|电话：|未填写|<', '', text).strip()
    #             # text = re.search(r'1\d{10}',text).group(0)
    #             text = "".join(re.findall(pattern, text))
    #             return text
    #         except:
    #             return ''
    #     else:
    #         return ''
    #
    # # 清洗电话号码
    # def search_telephone_num(self, text):
    #     if text:
    #         try:
    #             pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
    #             text = re.sub(r'\s|\r|\t|\n|公司电话：|：|暂未提供|未填写', '', text).strip()
    #             text = "".join(re.findall(pattern, text))
    #             return text
    #         except:
    #             return ''
    #     else:
    #         return ''
    #
    # # 清洗传真号码
    # def search_contact_Fax(self, text):
    #     if text:
    #         try:
    #             pattern = re.compile(r'\(?0\d{2,3}[)-]?\d{7,8}', re.S)
    #             # '公司联系人：胡'
    #             text = re.sub(r'\s|\r|\t|\n|公司传真：|：|暂未提供|未填写', '', text).strip()
    #             text = "".join(re.findall(pattern, text))
    #             return text
    #         except:
    #             return ''
    #     else:
    #         return ''
    #
    # # 清洗url
    # def search_url(self, text):
    #     if text:
    #         try:
    #             pattern = re.compile(
    #                 r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|"
    #                 r"([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)", re.S)
    #             text = "".join(re.findall(pattern, text))
    #             return text
    #         except:
    #             return ''
    #
    #     else:
    #         return ''
    #
    # # 清洗email
    # def search_email(self, text):
    #     if text:
    #         try:
    #             pattern = re.compile(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", re.S)
    #             text = re.sub(r'\s|\r|\t|\n|邮箱：|：|暂未提供|无', '', text).strip()
    #             text = "".join(re.findall(pattern, text))
    #             return text
    #         except:
    #             return ''
    #     else:
    #         return ""
    #
    # # 清洗QQ
    # def search_QQ(self, text):
    #     if text:
    #         try:
    #             pattern = re.compile(r"([1-9]\d{4,10})", re.S)
    #             text = re.sub(r'\s|\r|\t|\n|QQ：|：|暂未提供|未填写', '', text).strip()
    #             text = "".join(re.findall(pattern, text))
    #             return text
    #         except:
    #             return ''
    #     else:
    #         return ''
    #
    # # 清洗联系人
    # def search_linkman(self, text):
    #     if text:
    #         try:
    #             # '公司联系人：林伙桥'
    #             # '王锦彬 先生 总经理'
    #             text = text.split(' ')[0].split('（')[0]
    #             # text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写', '', text)[:3]
    #             # text = re.sub(r'\s|\r|\n|\t|先生|女士|小姐|联系人：|公司联系人：|：|暂未提供|未填写', '', text)[:3]
    #             if text and len(text) > 3:
    #                 text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-', '', text)[:3]
    #                 return text
    #             else:
    #                 text = re.sub(r'\s|\r|\n|\t|联系人：|公司联系人：|：|暂未提供|未填写|-', '', text)
    #                 return text
    #         except:
    #             return ''
    #     else:
    #         return ''
    #
    # # 清洗地址
    # def search_address(self, text):
    #     if text:
    #         try:
    #             # '公司地址：中国  广东  广州  番禺区沙头街嘉品二街二号1栋1529'
    #             text = re.sub(r'\s|\r|\n|\t|地址|公司地址|公司地址：|：|暂未提供|未填写|\|/', '', text)
    #             return text
    #         except:
    #             return text
    #     else:
    #         return ''
    #
    # # def get_md5(self,value):
    # #     # if value:
    # #     result = md5(.encode()).hexdigest()
    # #     return result
    #     # return ''
    #
    #
    #
    # company_Name = scrapy.Field(
    #     input_processor=MapCompose(search_company),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # # company_id = scrapy.Field(
    # #     input_processor=MapCompose(get_md5(item["company_Name"])),
    # #     # 将list中的元素，通过“,”连接起来
    # #     output_processor=Join("")
    # # )
    #
    #
    # kind = scrapy.Field(
    #     input_processor=MapCompose(replace_ss,rinse_keywords),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # linkman = scrapy.Field(
    #     input_processor=MapCompose(search_linkman),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # phone = scrapy.Field(
    #     # 去掉评论
    #     input_processor=MapCompose(search_phone_num),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # telephone = scrapy.Field(
    #     # 去掉评论
    #     input_processor=MapCompose(search_telephone_num),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # contact_Fax = scrapy.Field(
    #     input_processor=MapCompose(search_contact_Fax),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # company_address = scrapy.Field(
    #     input_processor=MapCompose(search_address),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )
    #
    # Source = scrapy.Field(
    #     input_processor=MapCompose(),
    #     # 将list中的元素，通过“,”连接起来
    #     output_processor=Join("")
    # )












