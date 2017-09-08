# 抓取彩票500网站的双色球信息

import scrapy
import re
from caipiao.items import DoubleColorBallItem


class Cp500DCBSpider(scrapy.spiders.Spider):
    """
    抓取彩票500网站的双色球数据
    """

    # 是否要抓取历史所有期数
    __all = False

    def __init__(self, all=bool, *args, **kwargs):
        if all:
            self.__all = all == "True"
        super(Cp500DCBSpider, self).__init__(*args, **kwargs)

    name = "cp500dcb"
    allowed_domains = ["500.com"]
    start_urls = ["http://kaijiang.500.com/ssq.shtml"]

    def parse(self, response):
        self.logger.info("fetch all periods:%s", self.__all)
        if self.__all:
            periods = response.xpath("//div[contains(@class,'iSelectList')]/a/text()").extract()
            self.logger.info("fetch all periods,num:%d", len(periods))
            for p in periods:
                url = "http://kaijiang.500.com/shtml/ssq/" + p + ".shtml"
                yield scrapy.Request(url, callback=self.parse_item)
        else:
            yield self.parse_item(response)

    def parse_item(self, response):
        item = DoubleColorBallItem()
        item['period'] = response.xpath("//font[@class='cfont2']/strong/text()").extract_first()
        self.logger.info("------------------------------period:%s", item['period'])
        lottery_date = response.xpath("//td[@class='td_title01']/span[@class='span_right']/text()").extract_first()
        match_obj = re.match(r'开奖日期：(.*)兑奖截止日期：', lottery_date)
        if match_obj:
            item['lottery_date'] = match_obj.group(1)
            self.logger.info("------------------------------lottery_date:%s", item['lottery_date'])

        red_balls = response.xpath("//li[@class='ball_red']/text()").extract()
        self.logger.info("------------------------------red_balls:%s", red_balls)
        if len(red_balls) == 6:
            for i, j in enumerate(red_balls):
                item[('red_ball_' + str(i + 1))] = j
        else:
            self.logger.info("red_balls parse failed!")

        item['blue_ball'] = response.xpath("//li[@class='ball_blue']/text()").extract_first()
        self.logger.info("------------------------------blue_ball:%s", item['blue_ball'])

        order_balls_text = response.xpath("//table/tr[contains(td,'出球顺序：') and not(@align='center')]").extract_first()
        self.logger.info("------------------------------order_balls_text:%s", order_balls_text)
        match_order = re.match(r".*(\d{2}(\s\d{2}){5}).*", order_balls_text, re.M | re.S)
        if match_order:
            item['order_balls'] = match_order.group(1)
        else:
            self.logger.info("order_balls parse failed!")

        sales_jackpot = response.xpath("//span[contains(@class, 'cfont1')]/text()").extract()

        if len(sales_jackpot) == 2:
            item['sales_amt'] = sales_jackpot[0]
            item['jackpot_amt'] = sales_jackpot[1]
        else:
            self.logger.info("sales_jackpot parse failed")

        kjs = response.xpath("//table[@class='kj_tablelist02'][last()]/tr[@align='center']")
        if len(kjs) == 7:
            for i, j in enumerate(kjs):
                if i == 0:
                    continue
                kj = j.xpath("td/text()").extract()
                item['prize_' + str(i) + '_num'] = kj[1].replace("\r", "").replace("\n", "").replace("\t", "")
                item['prize_' + str(i) + '_amt'] = kj[2].replace("\r", "").replace("\n", "").replace("\t", "")
        else:
            self.logger.info("prize parse failed")
        return item
