from scrapy import Spider
from scrapy.crawler import CrawlerProcess,CrawlerRunner
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import threading
import time
global crawlerProcessStarted
crawlerProcessStarted = False


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

def sleep(_,duration = 30):
	print(f'sleeping for: {duration}')
	time.sleep(duration)

def crawl(runner):
	d = runner.crawl(ScraperTest)
	d.addBoth(sleep)
	d.addBoth(lambda _: crawl(runner))
	return d

def loop_crawl(name):
	runner = CrawlerRunner(get_project_settings())
	crawl(runner)
	reactor.run()

if __name__ == "__main__":
	x = threading.Thread(target=loop_crawl,args=(1,))
	x.start()