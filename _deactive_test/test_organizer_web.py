from selenium.webdriver import Firefox
import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
import time
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "eager"
browser = Firefox(capabilities=caps)
import random


def test_organizer_create_event():
	browser.get("http://upcoming-events-platform.herokuapp.com/login")
	username = browser.find_element_by_id("username")
	password = browser.find_element_by_id("password")
	submit = browser.find_element_by_id("submit")
	username.send_keys('org1')
	password.send_keys('123')
	submit.click()

	url = browser.current_url
	assert url == "http://upcoming-events-platform.herokuapp.com/", "Test Failed"
	organizer_page = browser.find_element_by_xpath("/html/body/nav/div/div/ul/li[3]/a")
	organizer_page.click()
	assert browser.current_url == "http://upcoming-events-platform.herokuapp.com/panel/organizer", "Error organizator"

	create_event_page = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/form[2]/a")
	create_event_page.click()
	assert browser.current_url == "http://upcoming-events-platform.herokuapp.com/organizer/add/event"


	fields = browser.find_elements_by_class_name("form-control")
	for i,field in enumerate(fields,1):
		if(i == 2):
			continue
		else:
			field.send_keys("asd{}".format(random.randint(1,100)))	
	
	datefield = browser.find_element_by_xpath('//*[@id="date"]')
	datefield.click()
	datefield.send_keys("2020-10-10")
	time.sleep(2)
	add_event_button = browser.find_element_by_xpath('//*[@id="add_event"]')
	add_event_button.click()
	field = browser.find_element_by_id("name")
	assert field!=None, "Add event failed"
	assert field.text == "", "Add event failed"


def test_organizer_my_events():
	browser.get("http://upcoming-events-platform.herokuapp.com/panel/organizer")
	my_events_page = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/form[1]/a")
	my_events_page.click()
	assert browser.current_url == "http://upcoming-events-platform.herokuapp.com/myevents", "Error organizator"
	


if __name__ == "__main__":
	test_organizer_create_event()