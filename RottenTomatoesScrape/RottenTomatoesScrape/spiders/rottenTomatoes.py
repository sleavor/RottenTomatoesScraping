# -*- coding: utf-8 -*-
import scrapy
from RottenTomatoesScrape.items import RottentomatoesscrapeItem
from scrapy.spiders import CrawlSpider, Rule, SitemapSpider
import w3lib

class RottentomatoesSpider(SitemapSpider):
    name = 'rottenTomatoes'
    allowed_domains = ['www.rottentomatoes.com']
    sitemap_urls=['https://www.rottentomatoes.com/sitemap_0.xml']

    #Need to scrape sitemap_0.xml to sitemap_22.xml
#     for i in range(23):
#        sitemap_urls.append('https://www.rottentomatoes.com/sitemap_' + str(i) + '.xml')
    
    rules = [
        ('/pictures/', ''),
        ('/trailers/', ''),
        ('/m/', 'parse'),
    ]
    
    def parse(self, response):

        #Make sure that it is not a pictures or trailers page that is being crawled
        if '/pictures' in response.url or '/trailers' in response.url:
            if '/m/pictures' not in response.url or '/m/trailers' not in response.url:
                return
        
        item = RottentomatoesscrapeItem()

        #Grab all meta values and assign them if they exist - ignore if not
        a = response.xpath('//div[@class="meta-value"]').extract()
        b = response.xpath('//div[@class="meta-label subtle"]').extract()
        for c in range(len(b)):
            if "Genre:" in b[c]:
                genreList = []
                genres = w3lib.html.remove_tags(a[c]).replace("\n","").strip()
                for genre in genres.split(","):
                    genreList.append(genre.strip())
                item['genre'] = genreList
            elif "Rating:" in b[c]:
                item['rating'] = w3lib.html.remove_tags(a[c]).replace("\n", "").split(" ",1)[0].strip()
            elif "Directed By:" in b[c]:
                directorList = []
                directors = w3lib.html.remove_tags(a[c]).replace("\n", "").strip()
                for director in directors.split(","):
                    directorList.append(director.strip())
                item['director'] = directorList
            elif "Written By:" in b[c]:
                writerList = []
                writers = w3lib.html.remove_tags(a[c]).replace("\n","").strip()
                for writer in writers.split(","):
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
        
        #Get rest of data
        criticRate = response.xpath('//*[@id="tomato_meter_link"]/span[2]/text()').extract()
        audienceRate = response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/h2/a/span[2]/text()').extract()
        if criticRate:
            item['criticRate'] = int(criticRate[0].replace("\n", "").replace("%",""))
            item['numCritReviews'] = int(response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[1]/div/small/text()').extract()[0].replace("\n", "").replace(",",""))
        if audienceRate:
            item['audienceRate'] = int(audienceRate[0].replace("\n", "").replace("%",""))
            item['numAudienceReviews'] = int(response.xpath('//*[@id="topSection"]/div[2]/div[1]/section/section/div[2]/div/strong/text()').extract()[0].replace("User Ratings: ", "").replace(",",""))
        if audienceRate and criticRate:
            item['rateDiff'] = item['criticRate'] - item['audienceRate']
        item['title'] = response.xpath('//*[@id="topSection"]/div[2]/div[1]/h1/text()').extract()[0]
        
        yield item
