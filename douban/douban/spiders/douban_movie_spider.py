import scrapy
import re
import json
from douban.items import DoubanMovieItem
from scrapy.exceptions import CloseSpider


class DouBanMovieSpider(scrapy.spiders.Spider):
    # 抓取页数
    __page_num = 50

    def __init__(self, page_num=None, *args, **kwargs):
        if page_num:
            self.__page_num = int(page_num)
        super(DouBanMovieSpider, self).__init__(*args, **kwargs)

    name = "douban_movie"
    allowed_domains = ["douban.com"]
    '''
    https://movie.douban.com/explore#!type=movie&tag=热门&sort=recommend&page_limit=20&page_start=40
    '''
    start_urls = ["https://movie.douban.com/j/search_tags?type=movie&tag=热门&source="]

    def parse(self, response):
        tags_json = json.loads(response.body_as_unicode())
        for tag in tags_json["tags"]:
            self.logger.info("fetch tag:%s", tag)
            for i in range(0, self.__page_num * 20 + 1, 20):
                self.logger.info("fetch tag:%s,page_start:%s", tag, i)
                url = "https://movie.douban.com/j/search_subjects?type=movie&tag=" + tag + "&sort=time&page_limit=20&page_start=" + str(i)
                yield scrapy.Request(url, callback=self.parse_subjects_url)

    def parse_subjects_url(self, response):
        movie_json = json.loads(response.body_as_unicode())
        for film in movie_json["subjects"]:
            yield scrapy.Request(film['url'], callback=self.parse_film)

    def parse_film(self, response):
        if response.status == 403:
            raise CloseSpider("403 forbidden!")

        item = DoubanMovieItem()

        item['title'] = response.xpath("//span[@property='v:itemreviewed']/text()").extract_first()
        # self.logger.info("----------------title:%s", item['title'])

        item['directors'] = "/".join(response.xpath("//a[@rel='v:directedBy']/text()").extract())
        # self.logger.info("----------------directors:%s", item['directors'])

        item['adaptors'] = "/".join(response.xpath("//span[@class='attrs']/a[not(@rel)]/text()").extract())
        # self.logger.info("----------------adaptors:%s", item['adaptors'])

        item['starring'] = "/".join(response.xpath("//a[@rel='v:starring']/text()").extract())
        # self.logger.info("----------------starrings:%s", item['starring'])

        item['genre'] = "/".join(response.xpath("//span[@property='v:genre']/text()").extract())
        # self.logger.info("----------------genre:%s", item['genre'])

        info = response.xpath("//div[@id='info']").extract_first()
        s = re.search(r'制片国家/地区:</span>(.*)<br>.*<span class="pl">语言:</span>', info, re.M | re.S)
        if s:
            item['country'] = s.group(1)
            # self.logger.info("----------------country:%s", item['country'])

        item['release_date'] = "/".join(response.xpath("//span[@property='v:initialReleaseDate']/text()").extract())
        # self.logger.info("----------------release_date:%s", item['release_date'])

        item['runtime'] = response.xpath("//span[@property='v:runtime']/text()").extract_first()
        # self.logger.info("----------------runtime:%s", item['runtime'])

        item['rate'] = response.xpath("//strong[@property='v:average']/text()").extract_first()
        # self.logger.info("----------------rate:%s", item['rate'])
        return item
