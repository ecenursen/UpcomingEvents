from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector


class ScraperTest(Spider):
    name = "ScraperTest"
    allowed_domains = ["biletinial.com"]
    start_urls = ["https://www.biletinial.com/muzik"]

    def parse(self, response):
        events = Selector(response).xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div')
        for event in events:
            print(event.xpath(
                'a/div[@class="event-title"]/text()').extract()[0])


def scrape():
    print("Crawling process is starting...")
    process = CrawlerProcess()
    process.crawl(ScraperTest)
    print("Crawler attached...")
    process.start()
    print("Crawler finished...")
