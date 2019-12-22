# -*- coding: utf-8 -*-
import requests
import pytest
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))
from scraperTest import CemalResitRey, BiletiniAl, BaskaSinema, ScraperItem, months, trans_table
from scrapy.item import Field, Item
from scrapy.selector import Selector
sample_json = {"result": "OK", "message":"Sample"}

def test_valid_response_baskasinema():
	URLs = BaskaSinema.start_urls
	for url in URLs:
		response = requests.get(str(url))
		assert response.status_code == 200, "BaskaSinema 200 Response Failed for URL: {}".format(url)

def test_valid_response_biletinial():
	URLs = BiletiniAl.start_urls
	for url in URLs:
		response = requests.get(str(url))
		assert response.status_code == 200, "BiletiniAl 200 Response Failed for URL: {}".format(url)

def test_valid_response_crr():
	URLs = CemalResitRey.start_urls
	for url in URLs:
		response = requests.get(str(url))
		assert response.status_code == 200, "Cemal Resit Rey 200 Response Failed for URL: {}".format(url)

def test_valid_date_response_baskasinema():
	dateParser = BaskaSinema.parseDate
	assert dateParser(None,"28 Aralık 2019") == "2019-12-28", "BaskaSinema DateParser failed"
	assert dateParser(None,"1 Kasım 2020") == "2020-11-1", "BaskaSinema DateParser failed"
	assert dateParser(None,"2 Ocak 2021") == "2021-01-2", "BaskaSinema DateParser failed"

def test_valid_date_response_crr():
	dateParser = CemalResitRey.parseDate
	assert dateParser(None,"28 Aralık") == "2019-12-28", "CemalResitRey DateParser failed"
	assert dateParser(None,"1 Kasım") == "2020-11-1", "CemalResitRey DateParser failed"
	assert dateParser(None,"2 Ocak") == "2020-01-2", "CemalResitRey DateParser failed"

def test_valid_date_response_biletinial():
	dateParser = BiletiniAl.parseDate
	assert dateParser(None,"Aralık - 20") == ["2019-12-20"], "BiletiniAl DateParser failed"
	assert dateParser(None,"Aralık - 20 - 21 - 22") == ["2019-12-20", "2019-12-21","2019-12-22"], "BiletiniAl DateParser failed"
	assert dateParser(None,"Ocak - 1 - 10") == ["2020-01-1", "2020-01-10"], "BiletiniAl DateParser failed"