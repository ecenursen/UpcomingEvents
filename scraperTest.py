import threading
import time

from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


class BiletiniAlScraper(Spider):
	name = "BiletiniAlScraper"
    allowed_domains = ["biletinial.com"]
    start_urls = ["https://www.biletinial.com/muzik",
                  "https://biletinial.com/egitim", "https://biletinial.com/tiyatro",
                  "https://biletinial.com/spor", "https://biletinial.com/seminer", "https://biletinial.com/senfoni"]

    def parse(self, response):
        events = Selector(response).xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div')
		print("BiletiniAlScraper runs...")
		'''
        for event in events:
            item = ScraperItem()
            item['name'] = event.xpath(
                'a/div[@class="event-title"]/text()').extract()[0]
            item['url'] = "https://biletinial.com" + \
                event.xpath('a/@href').extract()[0]
            item['location'] = event.xpath(
                'a/div[@class="place"]/span/text()').extract()[0]
            item['city'] = event.xpath(
                'a/div[@class="place"]/span/b/text()').extract()[0]
            item['image'] = event.xpath(
                'a/img[@class="moimag"]/@data-path').extract()[0]
            item['date'] = ' '.join(s.strip().translate(trans_table)
                                    for s in event.xpath('a/ul/li/span/text()').extract())
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
        global f
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        f.write(line)
        yield item
		'''
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
		print("CRRScraper runs...")	
		'''
        for event in events:
            item = ScraperItem()
            item['date'] = event.xpath(
                'div[@class="dateColumn"]/span/text()').extract()[0]
            item['name'] = event.xpath(
                'div[@class="detailsColumn"]/div/div/h4/text()').extract()[0]
            item['type_'] = 'Konser'
            item['image'] = event.xpath(
                'div[@class="detailsColumn"]/div/img/@src').extract()[0]
            item['url'] = "https://crrkonsersalonu.ibb.istanbul/"+event.xpath(
                'div[@class="detailsColumn"]/div/a/@href').extract()[0]+"?CRRLang=tr-TR"
            item['location'] = 'Cemal Reşit Rey'
            item['city'] = 'İstanbul'
            item['description'] = ""
            global f
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            f.write(line)
            yield item
		'''
def sleep(_,duration = 60):
	print(f'sleeping for: {duration}')
	time.sleep(duration)

def crawl(runner):
	print("Biletini al")
	runner.crawl(BiletiniAlScraper)
	print("CRR")
	runner.crawl(CRRScraper)
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
