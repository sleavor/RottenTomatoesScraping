# -*- coding: utf-8 -*-
import scrapy
from RottenTomatoesScrape.items import RottentomatoesscrapeItem
from scrapy.spiders import CrawlSpider, Rule
import w3lib

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
                genreList = []
                genres = w3lib.html.remove_tags(a[c]).replace("\n","").strip()
                for genre in genres.split(",",1):
                    genreList.append(genre.strip())
                item['genre'] = genreList
            elif "Rating:" in b[c]:
                item['rating'] = w3lib.html.remove_tags(a[c]).replace("\n", "").split(" ",1)[0].strip()
            elif "Directed By:" in b[c]:
                item['director'] = w3lib.html.remove_tags(a[c]).replace("\n", "").strip()
            elif "Written By:" in b[c]:
                writerList = []
                writers = w3lib.html.remove_tags(a[c]).replace("\n","").strip()
                for writer in writers.split(",",1):
                    writerList.append(writer.strip())
                item['writer'] = writerList
            elif "In Theaters:" in b[c]:
                item['airDate'] = w3lib.html.remove_tags(a[c]).replace("\n", "").strip().split("  ",1)[0].strip()
            elif "Box Office:" in b[c]:
                item['boxOffice'] = int(w3lib.html.remove_tags(a[c]).replace("\n", "").replace("$","").replace(",",""))
            elif "Runtime:" in b[c]:
                item['runtime'] = w3lib.html.remove_tags(a[c]).replace("\n", "").strip()
            elif "Studio:" in b[c]:
                item['studio'] = w3lib.html.remove_tags(a[c]).replace("\n", "").strip()
        item['criticRate'] = int(response.xpath('//*[@id="tomato_meter_link"]/span[2]/text()').extract()[0].replace("\n", "").replace("%",""))
        item['numCritReviews'] = int(response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[1]/div/small/text()').extract()[0].replace("\n", "").replace(",",""))
        item['audienceRate'] = int(response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]/text()').extract()[0].replace("\n", "").replace("%",""))
        item['numAudienceReviews'] = int(response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/div/strong/text()').extract()[0].replace("User Ratings: ", "").replace(",",""))
        item['rateDiff'] = item['criticRate'] - item['audienceRate']
        item['title'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/h1/text()').extract()[0]
        yield item
