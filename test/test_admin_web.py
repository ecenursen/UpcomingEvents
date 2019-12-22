from selenium.webdriver import Firefox
import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
import time
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "eager"
browser = Firefox(capabilities=caps)
import random


def test_organizer_list_organizers():
	browser.get("http://upcoming-events-platform.herokuapp.com/login")
	username = browser.find_element_by_id("username")
	password = browser.find_element_by_id("password")
	submit = browser.find_element_by_id("submit")
	username.send_keys('ADMIN')
	password.send_keys('123')
	submit.click()

	url = browser.current_url
	assert url == "http://upcoming-events-platform.herokuapp.com/", "Test Failed"
	organizer_page = browser.find_element_by_xpath("/html/body/nav/div/div/ul/li[3]/a")
	organizer_page.click()
	assert browser.title != "Page not found :(", "Error"

	create_event_page = browser.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/form[2]/a")
	create_event_page.click()
	assert browser.title != "Page not found :(", "Error"