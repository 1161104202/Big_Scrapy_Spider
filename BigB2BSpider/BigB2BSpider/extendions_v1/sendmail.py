# import logging
# from scrapy import signals
# from scrapy.exceptions import NotConfigured
# from scrapy.mail import MailSender
#
#
# logger = logging.getLogger(__name__)
#
# class SendEmail(object):
#     def __init__(self,sender,item_count):
#         self.sender = sender
#         self.item_count = item_count
#         self.items_scraped = 0
#
#
#     @classmethod
#     def from_crawler(cls,crawler):
#         # first check if the extension should be enabled and raise
#         # NotConfigured otherwise
#         if not crawler.settings.getbool('MYEXT_ENABLED'):
#             raise NotConfigured
#
#         # get the number of items from settings
#         item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)
#
#         # instantiate the extension object
#         ext = cls(item_count,crawler)
#
#         # connect the extension object to signals
#         crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
#         crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
#         crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
#         crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
#
#
#         mail_host = crawler.settings.get('MAIL_HOST') # 发送邮件的服务器
#         mail_port = crawler.settings.get('MAIL_PORT') # 邮件端口
#         mail_user = crawler.settings.get('MAIL_USER') # 邮件发送者
#         # mail_receiver = crawler.settings.get('MAIL_Receiver')  # 邮件接收者
#         mail_pass = crawler.settings.get('MAIL_PASS') # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
#
#         sender = MailSender(mail_host,mail_user,mail_user,mail_pass,mail_port) #由于这里邮件的发送者和邮件账户是同一个就都写了mail_user了
#         print(type(sender))
#         h = cls(sender,crawler)
#
#         # return the extension object
#         return ext,h
#
#     def spider_idle(self,spider):
#         logger.info('idle spider %s' % spider.name)
#
#     def spider_opened(self, spider):
#         logger.info("opened spider {}".format(spider.name))
#         body = 'spider[{}] is opened'.format(spider.name)
#         subject = '[{}] good opened !!!'.format(spider.name)
#         return self.sender.send(to={'184108270@qq.com'}, subject=str(subject).encode("utf-8"), body=str(body).encode("utf-8"))
#
#     def item_scraped(self, item, spider):
#         self.items_scraped += 1
#         if int(self.items_scraped) % int(self.item_count) == 0:
#             logger.info("scraped {} items".format(self.items_scraped))
#             body = 'spider[{}] is scraped'.format(spider.name)
#             subject = '[{}] good scraped [{}] !!!'.format(spider.name,self.items_scraped)
#             return self.sender.send(to={'184108270@qq.com'}, subject=str(subject).encode("utf-8"), body=str(body).encode("utf-8"))
#
#     def spider_closed(self, spider):
#         logger.info("closed spider {}".format(spider.name))
#         body = 'spider[{}] is closed'.format(spider.name)
#         subject = '[{}] good closed !!!'.format(spider.name)
#         # self.sender.send(to={'zfeijun@foxmail.com'}, subject=subject, body=body)
#         return self.sender.send(to={"184108270@qq.com"}, subject=str(subject).encode("utf-8"), body=str(body).encode("utf-8"))
#
#

import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender


logger = logging.getLogger(__name__)

class SendEmail(object):
    def __init__(self,sender,crawler):
        self.sender = sender
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        mail_host = crawler.settings.get('MAIL_HOST') # 发送邮件的服务器
        mail_port = crawler.settings.get('MAIL_PORT') # 邮件发送端口
        mail_user = crawler.settings.get('MAIL_USER') # 邮件发送者
        mail_pass = crawler.settings.get('MAIL_PASS') # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！

        sender = MailSender(mail_host,mail_user,mail_user,mail_pass,mail_port) #由于这里邮件的发送者和邮件账户是同一个就都写了mail_user了
        h = cls(sender,crawler)

        return h

    def spider_idle(self,spider):
        logger.info('idle spider %s' % spider.name)

    def spider_closed(self, spider):
        logger.info("closed spider %s", spider.name)
        body = 'spider[%s] is closed' %spider.name
        subject = '[%s] good!!!' %spider.name
        # self.sender.send(to={'zfeijun@foxmail.com'}, subject=subject, body=body)
        return self.sender.send(to={'184108270@qq.com'}, subject=subject, body=body)
