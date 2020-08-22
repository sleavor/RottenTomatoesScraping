# -*- coding: utf-8 -*-
import scrapy
from RottenTomatoesScrape.items import RottentomatoesscrapeItem
from scrapy.spiders import CrawlSpider, Rule

class RottentomatoesSpider(scrapy.Spider):
    name = 'rottenTomatoes'
    allowed_domains = ['www.rottentomatoes.com']
    start_urls = ['https://www.rottentomatoes.com/m/kicking_and_screaming',
                'https://www.rottentomatoes.com/m/star_wars_episode_iii_revenge_of_the_sith'
    ]

    def parse(self, response):
        item = RottentomatoesscrapeItem()
        a = response.xpath('//div[@class="meta-value"]').extract()
        b = response.xpath('//div[@class="meta-label subtle"]').extract()
        for c in range(len(b)):
            if "Genre:" in b[c]:
                item['genre'] = a[c]
            elif "Rating:" in b[c]:
                item['rating'] = a[c]
            elif "Directed By:" in b[c]:
                item['director'] = a[c]
            elif "Written By:" in b[c]:
                item['writer'] = a[c]
            elif "In Theaters:" in b[c]:
                item['airDate'] = a[c]
            elif "Box Office:" in b[c]:
                item['boxOffice'] = a[c]
            elif "Runtime:" in b[c]:
                item['runtime'] = a[c]
            elif "Studio:" in b[c]:
                item['studio'] = a[c]
        item['criticRate'] = response.xpath('//*[@id="tomato_meter_link"]/span[2]/text()').extract()
        item['numCritReviews'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[1]/div/small/text()').extract()
        item['audienceRate'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]/text()').extract()
        item['numAudienceReviews'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/div/strong/text()').extract()
        #item['rateDiff'] = item['criticRate'] - item['audienceRate']
        item['title'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/h1/text()').extract()
        yield item
