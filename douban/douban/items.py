# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    """
    豆瓣电影
    """
    # 电影名
    title = scrapy.Field()
    # 导演
    directors = scrapy.Field()
    # 编剧
    adaptors = scrapy.Field()
    # 主演
    starring = scrapy.Field()
    # 类型
    genre = scrapy.Field()
    # 制片国家/地区
    country = scrapy.Field()
    # 上映日期
    release_date = scrapy.Field()
    # 时长 分钟
    runtime = scrapy.Field()
    # 豆瓣评分
    rate = scrapy.Field()
