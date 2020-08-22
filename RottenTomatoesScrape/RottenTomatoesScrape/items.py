# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RottentomatoesscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    criticRate = scrapy.Field()
    numCritReviews = scrapy.Field()
    audienceRate = scrapy.Field()
    numAudienceReviews = scrapy.Field()
    rateDiff = scrapy.Field()
    title = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    airDate = scrapy.Field()
    boxOffice = scrapy.Field()
    runtime = scrapy.Field()
    studio = scrapy.Field()