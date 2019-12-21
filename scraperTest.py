import datetime
import json
import time

from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.http import Request
from scrapy.item import Field, Item
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from server import add_scrapped
trans_table = {ord(c): None for c in u'\r\n\t'}


class ScraperItem(Item):
	name = Field()
	url = Field()
	date = Field()
	location = Field()
	city = Field()
	image = Field()
	date = Field()
	type_ = Field()
	description = Field()


class BiletiniAlScraper(Spider):
	name = "BiletiniAlScraper"
	allowed_domains = ["biletinial.com"]
	start_urls = ["https://www.biletinial.com/muzik",
				  "https://biletinial.com/egitim", "https://biletinial.com/tiyatro",
				  "https://biletinial.com/spor", "https://biletinial.com/seminer", "https://biletinial.com/senfoni"]

	def parse(self, response):
		events = Selector(response).xpath(
			'/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div')

		for event in events:
			'''
			global eventCounter
			print("Scraping:", eventCounter, "Biletinial")
			eventCounter += 1
			'''
			date = ' '.join(s.strip().translate(trans_table)
									for s in event.xpath('a/ul/li/span/text()').extract())
			dates = self.parseDate(date)
			for date in dates:
				item = ScraperItem()
				item['name'] = event.xpath(
					'a/div[@class="event-title"]/text()').extract()[0]
				item['date'] = date
				item['url'] = "https://biletinial.com" + \
					event.xpath('a/@href').extract()[0]
				
				item['location'] = event.xpath(
					'a/div[@class="place"]/span/text()').extract()[0]
				item['city'] = event.xpath(
					'a/div[@class="place"]/span/b/text()').extract()[0]
				item['image'] = event.xpath(
					'a/img[@class="moimag"]/@data-path').extract()[0]
				item['type_'] = event.xpath(
					'a/div[@class="category"]/text()').extract()[0]
				
				request = Request(
					url=item['url'], callback=self.get_description, meta={'item': item})
				yield request
	
	def get_description(self, response):
		page = Selector(response)
		item = ScraperItem(response.meta["item"])
		item['description'] = ' '.join(s.strip().translate(
			trans_table) for s in page.xpath('//*[@id="movie-detail"]//p/text()').extract())
		print(add_event(item['name'],item['city'],item['location'],item['date'],item['type_'],item['url'],item['image']))
	
	def parseDate(self, date):
		dateStr = date.replace(" ","").split("-")  

		eventMonth = months.index(dateStr[0])+1
		days = dateStr[1:]    
		
		dates = []
		currentMonth = datetime.datetime.today().month
		currentYear = datetime.datetime.today().year
		for day in days:
			eventYear = currentYear+1 if eventMonth-currentMonth<0 else currentYear
			if(eventMonth < 10):
				month = "0{}".format(eventMonth)
			else:
				month = "{}".format(eventMonth)
			dateString="{}-{}-{}".format(eventYear,month,day)
			dates.append(dateString)
		return dates

class CRRScraper(Spider):
	name = "CRRScraper"
	allowed_domains = ["crrkonsersalonu.ibb.istanbul"]
	start_date = time.strftime("%d.%m.%y")
	end_date = (datetime.datetime.now() + datetime.timedelta(100)
				).isoformat()[:10].replace('-', '.')
	end_date = end_date[-2:] + "." + end_date[5:-3] + "." + end_date[:4]
	start_urls = [
		"https://crrkonsersalonu.ibb.istanbul/Home/Events?CRRLang=tr-TR&startDate={}&endDate={}&dateRange=0&categoryId=0".format(start_date, end_date)]
		
	def parse(self, response):

		events = Selector(response).xpath(
			'/html/body/div[2]/div/div[3]/div/div[3]/div')
		for event in events:
			item = ScraperItem()
			item['name'] = event.xpath(
				'div[@class="detailsColumn"]/div/div/h4/text()').extract()[0]
			date = self.parseDate(event.xpath(
				'div[@class="dateColumn"]/span/text()').extract()[0])
			item['date'] = date
			item['type_'] = 'Konser'
			item['image'] = event.xpath(
				'div[@class="detailsColumn"]/div/img/@src').extract()[0]
			item['url'] = "https://crrkonsersalonu.ibb.istanbul/"+event.xpath(
				'div[@class="detailsColumn"]/div/a/@href').extract()[0]+"?CRRLang=tr-TR"
			item['location'] = 'Cemal Reşit Rey'
			item['city'] = 'İstanbul'
			item['description'] = ""
			print(add_event(item['name'],item['city'],item['location'],item['date'],item['type_'],item['url'],item['image']))
			

	def parseDate(self,date):
		date=date.split(" ")
		eventMonth = months.index(date[1])+1
		day = date[0]
		
		currentMonth = datetime.datetime.today().month
		currentYear = datetime.datetime.today().year
		eventYear = currentYear+1 if eventMonth-currentMonth<0 else currentYear
		if(eventMonth < 10):
			month = "0{}".format(eventMonth)
		else:
			month = "{}".format(eventMonth)
		dateString="{}-{}-{}".format(eventYear,month,day)
		return dateString

class BaskaSinema(Spider):

	name = "BaskaSinemaScraper"
	allowed_domains = ["baskasinema.com"]
	start_urls = ["http://www.baskasinema.com/gelecek-filmler/", ]

	def parse(self, response):
		events = Selector(response).xpath(
			'/html/body/div[2]/div[2]/div/div/div[2]/div[2]/div')

		for event in events:
			'''
			global eventCounter
			print("Scraping:", eventCounter, "baskasinema")
			eventCounter += 1
			'''
			item = ScraperItem()
			date = event.xpath(
				'div[@class="movie_info_box"]/div[@class="movie_info"]/strong/text()').extract()[0]
			item['date'] = self.parseDate(date)
			item['name'] = event.xpath(
				'div[@class="movie_info_box"]/h2/span/text()').extract()[0]
			item['type_'] = "Sinema"
			item['image'] = event.xpath('div/a/img/@src').extract()[0]
			item['url'] = event.xpath('div/a/@href').extract()[0]
			item['location'] = ""
			item['city'] = ""
			item['description'] = ' '.join(s.strip().translate(trans_table)
										   for s in event.xpath('div[@class="movie_info_box"]/div[@class="movie_info"]//text()').extract())
			print(add_event(item['name'],item['city'],item['location'],item['date'],item['type_'],item['url'],item['image']))

	def parseDate(self, date):
		date=date.split(" ")
		eventMonth = months.index(date[1])+1
		if(eventMonth < 10):
			month = "0{}".format(eventMonth)
		else:
			month = "{}".format(eventMonth)
		day = date[0]
		eventYear = date[2]
		dateString="{}-{}-{}".format(eventYear,month,day)
		return dateString


def sleep(_, duration=60):
	print(f'sleeping for: {duration}')
	time.sleep(duration)


def crawl(runner):
	runner.crawl(BiletiniAl)
	runner.crawl(CemalResitRey)
	runner.crawl(BaskaSinema)
	d = runner.join()
	d.addBoth(sleep)
	d.addBoth(lambda _: crawl(runner))
	return d


def loop_crawl():
	runner = CrawlerRunner(get_project_settings())
	print("Runner initialized")
	crawl(runner)
	reactor.run()


if __name__ == "__main__":
	print("Scraper test begins...")
	loop_crawl()
