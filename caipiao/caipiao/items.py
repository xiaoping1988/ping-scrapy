# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubleColorBallItem(scrapy.Item):
    """
    双色球
    """
    period = scrapy.Field()
    lottery_date = scrapy.Field()
    red_ball_1 = scrapy.Field()
    red_ball_2 = scrapy.Field()
    red_ball_3 = scrapy.Field()
    red_ball_4 = scrapy.Field()
    red_ball_5 = scrapy.Field()
    red_ball_6 = scrapy.Field()
    blue_ball = scrapy.Field()
    order_balls = scrapy.Field()
    sales_amt = scrapy.Field()
    jackpot_amt = scrapy.Field()
    prize_1_num = scrapy.Field()
    prize_1_amt = scrapy.Field()
    prize_2_num = scrapy.Field()
    prize_2_amt = scrapy.Field()
    prize_3_num = scrapy.Field()
    prize_3_amt = scrapy.Field()
    prize_4_num = scrapy.Field()
    prize_4_amt = scrapy.Field()
    prize_5_num = scrapy.Field()
    prize_5_amt = scrapy.Field()
    prize_6_num = scrapy.Field()
    prize_6_amt = scrapy.Field()

