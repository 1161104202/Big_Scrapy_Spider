#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

# 将start_url 存储到redis中的redis_key中，让爬虫去爬取
redis_Host = "127.0.0.1"
redis_key = 'ksb:start_urls'

# 创建redis数据库连接
rediscli = redis.Redis(host=redis_Host, port=6379, db="1")

# 先将redis中的requests全部清空
flushdbRes = rediscli.flushdb()
print("flushdbRes = {}".format(flushdbRes))
rediscli.lpush(redis_key, "http://www.kusoba.com/")
