# -*- coding: utf-8 -*-

# Scrapy settings for BigB2BSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
BOT_NAME = 'BigB2BSpider'

SPIDER_MODULES = ['BigB2BSpider.spiders']
NEWSPIDER_MODULE = 'BigB2BSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = "DEBUG"

# import datetime
# # startDate = datetime.datetime.now().strftime('%Y-%m-%d %A %H:%M:%S %f')
# log_startDate = datetime.datetime.now().strftime('%Y_%m_%d')
# LOG_FILE = f"BigB2BSpider_logs{log_startDate}.txt"
#
# import os
# path_file = LOG_FILE
# if not os.path.exists(path_file):
#     LOG_FILE = f"BigB2BSpider_logs{log_startDate}.txt"
# else:
#     print('File already exists')
#     pass


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    # "Cookie":"Hm_lvt_39b391b010992cf89654d83467db5db7=1564969344; Hm_lpvt_39b391b010992cf89654d83467db5db7=1564970833",
    # "Host":"www.mfqyw.com",
    # "Referer":"http://www.mfqyw.com/company/list-2426.html",
    # "Upgrade-Insecure-Requests":"1",
    # "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'BigB2BSpider.middlewares.Bigb2BspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'BigB2BSpider.middlewares.Bigb2BspiderDownloaderMiddleware': 543,
    'BigB2BSpider.middlewares.RandomMyProxyMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# EXTENSIONS = {
#     # 'scrapy.extensions.telnet.TelnetConsole': 300,
#     # 'BigB2BSpider.extendions.sendmail.SendEmail': 300,
#     'BigB2BSpider.extensions.closespider.CloseSpider': 300,
# }
# MYEXT_ENABLED = True

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  # 'BigB2BSpider.pipelines.Bigb2BspiderPipeline': 300,
  'BigB2BSpider.pipelines.MysqlTwistedPiplines': 301,
  'BigB2BSpider.pipelines.MysqlTwistedPiplines_v1': 302,
  # 'BigB2BSpider.pipelines.MongoPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '*****' # 你的密码
MYSQL_PORT = '3306'
MYSQL_DBNAME = 'bigdata'

# # 网易163邮箱
# MAIL_HOST = 'smtp.163.com'
# # 2> 配置服务的端口，默认的邮件端口是25.
# MAIL_PORT = 25
# # 3> 指定发件人和收件人。
# MAIL_USER = ''
# # 4> 授权码是用于登录第三方邮件客户端的专用密码。
# MAIL_PASS = ''
# # 4> 邮件接收者。
# mail_receiver = ""

# from datetime import datetime
# date = datetime.now()
# # 日志文件设置
# # LOG_LEVEL = 'DEBUG'
# # LOG_LEVEL = 'WARNING'
# LOG_ENCODING = 'utf-8'
# # 判断是否存在log文件夹，不存在则创建
# if os.path.exists('./log'):
#     print('Log folder already exists.Do nothing.')
# else:
#     print('There is no log folder for storage, create!')
#     os.makedirs('log')
# LOG_FILE = 'log/{}-{}-{}T{}_{}_{}.log'.format(date.year, date.month, date.day, date.hour, date.minute, date.second)
#
#
# # 错误数达到该值时结束爬虫且发送邮件
# CLOSESPIDER_ERRORCOUNT = 1
#
# # 发送邮件相关设置
# # 收件人
# STATSMAILER_RCPTS = ['1500132166@qq.com', '184108270@qq.com']
# # STATSMAILER_RCPTS = 'liuzc@jianshutech.com,chensy@jianshutech.com,weipan@jianshutech.com'
# # 项目名
# PROJECT_NAME = '爬虫指定数量错误关闭发送邮件测试'
# # 邮件发送服务器
# MAIL_HOST = 'smtp.163.com'
# # 发件人地址
# MAIL_FROM = '18942269545@163.com'
# # 授权码或者密码
# MAIL_PASS = 'ping1688'
# # 邮件发送服务器端口
# MAIL_PORT = 25

RETRY_ENABLED = True
RETRY_TIMES = 5
# RETRY_HTTP_CODES = [500,502,503,504,522,524,408]


# AUTOTHROTTLE_ENABLED = True,  # 启动[自动限速]
# AUTOTHROTTLE_DEBUG = True,  # 开启[自动限速]的debug
# AUTOTHROTTLE_MAX_DELAY = 10,  # 设置最大下载延时
# DOWNLOAD_TIMEOUT = 5, #设置下载超时
# CONCURRENT_REQUESTS_PER_DOMAIN = 4, # 限制对该网站的并发请求数


# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # 确保所有爬虫共享相同的去重指纹
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.LifoQueue'
# DB_IP = '127.0.0.1'
# dbNum = 6
# Redis_IP = '127.0.0.1'
# REDIS_URL = 'redis://{0}:6379/{1}'.format(Redis_IP, dbNum)
# # Persist 允许暂停
# SCHEDULER_PERSIST = True
# SCHEDULER_FLUSH_ON_START = False


# # 不验证SSL证书
# DOWNLOAD_HANDLERS_BASE = {
#     'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
#     'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
#     'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
#     's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
# }
# DOWNLOAD_HANDLERS = {
#     'https': 'BigB2BSpider.custom.downloader.handler.https.HttpsDownloaderIgnoreCNError',
# }

# allowed_domains = ['.*']


#
# import datetime
# MONGO_URI="127.0.0.1:27017"
# MONGO_DATABASE="all_spider_test"
# COLLECTION_NAME = f'B2B{datetime.datetime.now().strftime("%Y%m%d")}'

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # 确保所有爬虫共享相同的去重指纹
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # SCHEDULER_QUEUE_CLASS='scrapy_redis.queue.LifoQueue'
# DB_IP = 'localhost'
# dbNum = 1
# Redis_IP = 'localhost'
# REDIS_URL = 'redis://{0}:6379/{1}'.format(Redis_IP, dbNum)
# # Persist 允许暂停
# SCHEDULER_PERSIST = True
# SCHEDULER_FLUSH_ON_START = True


