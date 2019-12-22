# -*- coding: utf-8 -*-
import requests
import pytest
import os.path
import sys
import requests
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))

from server import *
from db_cursor import *

sample_json= {"name":"Sample","city":"İstanbul"}
sample_list = [0,0]
sample_str = "SAMPLE STRING"

################
#
# API TESTS
#
################

def test_api_login_admin():
    URL = "https://ituse19-uep.herokuapp.com/api/admin/login_verif"
    PARAMS = {'username':"ADMIN",'password': "123"}
    r = requests.get(url=URL,params=PARAMS)
    response = r.json()
    assert response["result"]==1,"Admin login failed"
    assert r.status_code==200, "Invalid Response"

def test_api_read_organizer():
    URL = "https://ituse19-uep.herokuapp.com/api/admin/all_organizers/"
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_list),"Read Organizer Function Fail"
    assert r.status_code==200, "Invalid Response"

def test_api_get_organizer_info():
    for org_id in range(10):
        URL = "https://ituse19-uep.herokuapp.com/api/get_organizer_info/{}".format(org_id)
        r = requests.get(url=URL)
        response = r.json()
        assert type(response)==type(sample_json) or type(response)==type(sample_list),"Read Organizer Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_organizer_verify():
    URL = "https://ituse19-uep.herokuapp.com/api/organizer_login_verif"
    PARAMS = {'username':"org1",'password': "123"}
    r = requests.get(url=URL,params=PARAMS)
    response = r.json()
    assert response["result"]==1,"Organizer login failed"
    assert r.status_code==200, "Invalid Response"

def test_api_read_organizer_review():
    URL = "https://ituse19-uep.herokuapp.com/api/admin/organizer_review"
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==type(sample_list),"Read Organizer Review Function Fail"
    assert r.status_code==200, "Invalid Response"

def test_api_add_organizer_review():
    URL = "https://ituse19-uep.herokuapp.com/api/register_organizer"
    PARAMS = {'name':"org2",'mail': "itu.edu.tr",'address':"blablastreet",'username': "org2",'password': "123"}
    r = requests.post(url=URL,params=PARAMS)
    response = r.json()
    assert type(response)==type(sample_json),"Add Organizer Review Function Fail"
    assert r.status_code==200, "Invalid Response"
    delete("ORGANIZER_REVIEW","NAME='org2' AND MAIL='itu.edu.tr' AND ADDRESS='blablastreet' AND USERNAME='org2' AND PASSWORD='123'")

def test_api_organizer_review_approve():
    for org_id in range(3):
        URL = "https://ituse19-uep.herokuapp.com/api/admin/organizer_approve/{}".format(org_id)
        r = requests.post(url=URL)
        response = r.json()
        assert type(response)==type(sample_json) or type(response)==str,"Organizer Review Approve Function Fail"
        assert r.status_code==200, "Invalid Response"
    


################
#
# COVARAGE TESTS
#
################

def test_cov_is_admin():
    response = is_admin("ADMIN","123")
    assert response["result"]==1,"Admin login failed"

def test_cov_add_admin():
    response = add_admin("ADMIN2","1234")
    assert response["result"]==1 or response["result"]==-1,"Admin add failed"
    delete("ADMIN","WHERE USERNAME='ADMIN2' AND PASSWORD='1234'")

def test_cov_read_organizer():
    response = read_organizer()
    assert type(response)==type(""),"Read Organizer Function Fail"

def test_cov_get_organizer_info():
    for org_id in range(10):
        response = get_organizer_info(org_id)
        assert type(response)==type("") or type(response)==type(sample_json),"Read Organizer Function Fail"

def test_cov_add_organizer():
    response = add_organizer("NAME","MAIL","ADDRESS")
    assert type(response)==type(sample_json),"Add Organizer Function Fail"
    delete("ORGANIZER"," NAME='NAME' AND MAIL='MAIL' AND ADDRESS='ADDRESS'")

def test_cov_add_organizer_login():
    response = add_organizer_login(1,"username","password")
    assert type(response)==type(sample_json),"Add Organizer Login Function Fail"
    delete("ORGANIZER_LOGIN"," USERNAME='username' AND PASSWORD='password' AND ORGANIZER_ID=CAST '1' AS INTEGER")

def test_cov_organizer_verify():
    response = organizer_verify("org1","123")
    assert type(response)==type(sample_json),"Organizer Verify Function Fail"

def test_cov_read_organizer_review():
    response = read_organizer_review()
    assert type(response)==type("") or type(response)==type(sample_json),"Read Organizer Review Function Fail"

def test_cov_add_organizer_review():
    response = add_organizer_review("org2","itu.edu.tr","blablastreet","org2","123")
    assert type(response)==type(sample_json),"Add Organizer Review Function Fail"
    #delete("ORGANIZER_REVIEW","NAME='org2' AND MAIL='itu.edu.tr' AND ADDRESS='blablastreet' AND USERNAME='org2' AND PASSWORD='123'")

def test_cov_organizer_review_approve():
    for org_id in range(10):
        response = organizer_review_approve(org_id)
        assert type(response)==type(sample_json),"Organizer Review Approve Function Fail"
