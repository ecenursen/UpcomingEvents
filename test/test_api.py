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
    #delete("ORGANIZER_REVIEW","NAME='org2' AND MAIL='itu.edu.tr' AND ADDRESS='blablastreet' AND USERNAME='org2' AND PASSWORD='123'")

def test_api_organizer_review_approve():
    for org_id in range(3):
        URL = "https://ituse19-uep.herokuapp.com/api/admin/organizer_approve/{}".format(org_id)
        r = requests.post(url=URL)
        response = r.json()
        assert type(response)==type(sample_json) or type(response)==str,"Organizer Review Approve Function Fail"
        assert r.status_code==200, "Invalid Response"
    
def test_api_organizer_review_reject():
    for org_id in range(3):
        URL = "https://ituse19-uep.herokuapp.com/api/admin/organizer_reject/{}".format(org_id)
        r = requests.delete(url=URL)
        response = r.json()
        assert type(response)==type(sample_json),"Organizer Review Reject Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_read_events():
    URL = "https://ituse19-uep.herokuapp.com/api/events/{}".format(100)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Read Events Function Fail"
    assert r.status_code==200, "Invalid Response"

def test_api_read_organizers_events():
    for org_id in range(10):
        URL = "https://ituse19-uep.herokuapp.com/api/events/{}".format(org_id)
        r = requests.get(url=URL)
        response = r.json()
        assert type(response)==type(sample_json) or type(response)==list,"Read Organizer's Events Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_read_event():
    for e_id in range(10):
        URL = "https://ituse19-uep.herokuapp.com/api/event_detail/{}".format(e_id)
        r = requests.get(url=URL)
        response = r.json()
        assert type(response)==type(sample_json) or type(response)==list,"Event Detail Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_delete_event():
    for e_id in range(10):
        URL = "https://ituse19-uep.herokuapp.com/api/delete_event/{}".format(e_id)
        r = requests.delete(url=URL)
        response = r.json()
        assert type(response)==type(sample_json) or type(response)==list,"Delete Event Function Fail"
        assert r.status_code==200, "Invalid Response"


def test_api_filter_search():
    (keyword,city,e_type) = ("None","None","None")
    URL="https://ituse19-uep.herokuapp.com/api/filter_search/{}/{}/{}".format(keyword,city,e_type)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Filter Search Function Fail"
    assert r.status_code==200, "Invalid Response"

    (keyword,city,e_type) = ("den","Ağrı","None")
    URL="https://ituse19-uep.herokuapp.com/api/filter_search/{}/{}/{}".format(keyword,city,e_type)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Filter Search Function Fail"
    assert r.status_code==200, "Invalid Response"

    (keyword,city,e_type) = ("None","İstanbul","None")
    URL="https://ituse19-uep.herokuapp.com/api/filter_search/{}/{}/{}".format(keyword,city,e_type)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Filter Search Function Fail"
    assert r.status_code==200, "Invalid Response"

    (keyword,city,e_type) = ("None","None","Konser")
    URL="https://ituse19-uep.herokuapp.com/api/filter_search/{}/{}/{}".format(keyword,city,e_type)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Filter Search Function Fail"
    assert r.status_code==200, "Invalid Response"

    (keyword,city,e_type) = ("Yılbaşı","None","None")
    URL="https://ituse19-uep.herokuapp.com/api/filter_search/{}/{}/{}".format(keyword,city,e_type)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Filter Search Function Fail"
    assert r.status_code==200, "Invalid Response"

def test_api_read_event_review():
    URL="https://ituse19-uep.herokuapp.com/api/admin/event_review"
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json) or type(response)==list,"Read Event Review Function Fail"
    assert r.status_code==200, "Invalid Response"


def test_api_new_event():
    for org_id in range(1,10):
        URL="https://ituse19-uep.herokuapp.com/api/add_new_event/{}".format(org_id)
        (name,city,location,date,e_type,description,image,ticket_url) = ("eventreview1","istanbul","location","2019-12-26","konser","bsnfbmsbf","jsebfjhb.jpeg","nsebfj.com")
        PARAMS = {'name':name,'city':city,"location":location,"date": date,"type":e_type,"description":description,"image":image,"ticket_url":ticket_url}
        r = requests.post(url=URL,params=PARAMS)
        response = r.json()
        assert type(response)==type(sample_json),"Add New Event to Review Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_update_event():
    for old_event_id in range(1,10):
        (name,city,location,date,e_type,description,image,ticket_url) = ("eventreview1","istanbul","location","2019-12-26","konser","bsnfbmsbf","jsebfjhb.jpeg","nsebfj.com")
        URL="https://ituse19-uep.herokuapp.com/api/event_update"
        PARAMS = {'name':name,'city':city,"location":location,"date": date,"type":e_type,"description":description,"image":image,"ticket_url":ticket_url,"org_id":1,"old_event_id":old_event_id}
        r = requests.post(url=URL,params=PARAMS)
        response = r.json()
        assert type(response)==type(sample_json),"Add Updated Event to Review Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_new_event_review_approve():
    for e_id in range(100):
        URL="https://ituse19-uep.herokuapp.com/api/admin/new_event_approve/{}".format(e_id)
        r = requests.post(url=URL)
        response = r.json()
        assert type(response)==type(sample_json),"New Event Approve Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_updated_event_review_approve():
    for e_id in range(100):
        URL="https://ituse19-uep.herokuapp.com/api/admin/updated_event_approve/{}".format(e_id)
        r = requests.put(url=URL)
        response = r.json()
        assert type(response)==type(sample_json),"Updated Event Approve Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_event_review_reject():
    for e_id in range(100):
        URL="https://ituse19-uep.herokuapp.com/api/admin/event_reject/{}".format(e_id)
        r = requests.delete(url=URL)
        response = r.json()
        assert type(response)==type(sample_json),"Event from Review Rejected Function Fail"
        assert r.status_code==200, "Invalid Response"

def test_api_username_verif():
    username = "org2"
    URL="https://ituse19-uep.herokuapp.com/api/username_control/{}".format(username)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json),"Username Verify Function Fail"
    assert r.status_code==200, "Invalid Response"

    username = ""
    URL="https://ituse19-uep.herokuapp.com/api/username_control/{}".format(username)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json),"Username Verify Function Fail"
    assert r.status_code==200, "Invalid Response"

    username = "organizerimben2"
    URL="https://ituse19-uep.herokuapp.com/api/username_control/{}".format(username)
    r = requests.get(url=URL)
    response = r.json()
    assert type(response)==type(sample_json),"Username Verify Function Fail"
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

def test_cov_organizer_review_reject():
    for org_id in range(10):
        response = organizer_review_reject(org_id)
        assert type(response)==type(sample_json),"Organizer Review Reject Function Fail"

def test_cov_read_events():
    response = read_events(1000)
    assert type(response)==str,"Read Events Function Fail"

def test_cov_read_organizers_events():
    for org_id in range(10):
        response = read_organizers_events(org_id)
        assert type(response)==str or type(response)==dict,"Read Organizer's Events Function Fail"

def test_cov_read_event():
    for e_id in range(100):
        response = read_event(e_id)
        assert type(response)==str or type(response)==dict,"Event Detail Function Fail"

def test_cov_add_event():
    response = add_event("event12","istanbul","crr","2019-12-25","konser","sefs.com")
    assert type(response)==type(sample_json),"Add Event Function Fail"

def test_cov_delete_event():
    for e_id in range(10):
        response = delete_event(e_id)
        assert type(response)==type(sample_json),"Delete Event Function Fail"

def test_cov_filter_search():
    response = filter_search("None","None","None")
    assert type(response)==str or type(response)==dict,"Filter Search Function Fail"
    response = filter_search("den","Ağrı","None")
    assert type(response)==str or type(response)==dict,"Filter Search Function Fail"
    response = filter_search("None","İstanbul","None")
    assert type(response)==str or type(response)==dict,"Filter Search Function Fail"
    response = filter_search("None","None","Konser")
    assert type(response)==str or type(response)==dict,"Filter Search Function Fail"
    response = filter_search("Yılbaşı","None","None")
    assert type(response)==str or type(response)==dict,"Filter Search Function Fail"

def test_cov_read_event_review():
    response = read_event_review()
    assert type(response)==str or type(response)==dict,"Read Event Review Function Fail"

def test_cov_add_event_review():
    (name,city,location,date,e_type,org_id) = ("eventreview1","istanbul","location","2019-12-26","konser",1)
    response = add_event_review(name,city,location,date,e_type,org_id)
    assert type(response)==type(sample_json),"Add Event Review Function Fail"

    (name,city,location,date,e_type,org_id,old_evet_id) = ("eventreview1","istanbul","location","2019-12-26","konser",1,250)
    response = add_event_review(name,city,location,date,e_type,org_id,old_evet_id=old_evet_id)
    assert type(response)==type(sample_json),"Add Event Review Function Fail"

def test_cov_new_event():
    for org_id in range(10):
        (name,city,location,date,e_type,description,image,ticket_url) = ("eventreview1","istanbul","location","2019-12-26","konser","bsnfbmsbf","jsebfjhb.jpeg","nsebfj.com")
        response = new_event(org_id,name,city,location,date,e_type, description,image,ticket_url)
        assert type(response)==type(sample_json),"Add New Event to Review Function Fail"

def test_cov_update_event():
    for old_event_id in range(100):
        (name,city,location,date,e_type,description,image,ticket_url) = ("eventreview1","istanbul","location","2019-12-26","konser","bsnfbmsbf","jsebfjhb.jpeg","nsebfj.com")
        response = update_event(old_event_id,1,name,city,location,date,e_type,description,image,ticket_url)
        assert type(response)==type(sample_json),"Add Updated Event to Review Function Fail"

def test_cov_new_event_review_approve():
    for e_id in range(10):
        response = new_event_review_approve(e_id)
        assert type(response)==type(sample_json),"New Event Approved Function Fail"

def test_cov_updated_event_review_approve():
    for e_id in range(10):
        response = updated_event_review_approve(e_id)
        assert type(response)==type(sample_json),"Updated Event Approved Function Fail"

def test_cov_event_review_reject():
    for e_id in range(10):
        response = event_review_reject(e_id)
        assert type(response)==type(sample_json),"Event from Review Rejected Function Fail"

def test_cov_username_verif():
    username = "org2"
    response = username_verif(username)
    assert type(response)==type(sample_json),"Username Verify Function Fail"
    
    username = ""
    response = username_verif(username)
    assert type(response)==type(sample_json),"Username Verify Function Fail"
    
    username = "organizerimben2"
    response = username_verif(username)
    assert type(response)==type(sample_json),"Username Verify Function Fail"
    