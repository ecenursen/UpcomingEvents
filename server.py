import os,sys
from flask import Flask, jsonify, request
from dbinit import initialize,drop_table
import psycopg2 as db
import json
from datetime import datetime,timedelta
from db_cursor import select,insert,update,delete,search
db.extensions.register_type(db.extensions.UNICODE)
db.extensions.register_type(db.extensions.UNICODEARRAY)

DEBUG = False

class return_query(dict):

	def __init__ (self):
		self = dict()

	def add(self,key,value):
		self[key] = value

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['JSON_AS_ASCII'] = False

########################
#
# FUNCTIONS ARE IN THE
# SAME ORDER WITH DB
#
########################
#
# EVERY TABLE FUNCTION
# IN THE ORDER OF CRUD
#
########################


########################
#
# ADMIN TABLE 
#
########################

def add_admin(username,password):
	result = insert("USERNAME,PASSWORD","ADMIN", "'"+username +"','" + password+"'")
	return result
	
@app.route('/api/admin/login_verif',methods=['GET'])
def is_admin():
	username = request.form['username']
	password = request.form['password']
	others = "WHERE USERNAME=" + "CAST('"+str(username)+"' AS VARCHAR) " + "AND PASSWORD=" + "CAST('"+str(password)+"' AS VARCHAR) "
	result = select("*","ADMIN",others)
	if(type(result)==type([0,0])):
		result = {"result":1,"message" :"Login verified"}
	return result

########################
# 
# ORGANIZER TABLE
#
########################

@app.route('/api/all_organizers/', methods=['GET'])
def read_organizer():
	query = return_query()
	result = select("ID,NAME,MAIL,ADDRESS","ORGANIZER")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"mail": row[2],
			"address": row[3]
		})
	return  jsonify(query)

@app.route('/api/get_organizer_info/<int:org_id>',methods=['GET'])
def get_organizer_info(org_id):
	query = return_query()
	result = select("ID,NAME,MAIL,ADDRESS","ORGANIZER","WHERE ID="+ "CAST('"+str(org_id)+"' AS INTEGER) ")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"mail": row[2],
			"address": row[3]
		})
	return  jsonify(query)

def add_organizer(name,mail=" ",address="empty"):
	duplicate = select("*","ORGANIZER","WHERE NAME='"+name+"' AND MAIL='" +mail+"' AND ADDRESS='"+ address + "'")
	if(type(duplicate)==type([0,0])):
		print("\n\nDUPLICATED ORGANIZER ALERT\n")
		return {"result":-1,"message":"Duplicated Organizer"}
	result = insert("NAME,MAIL,ADDRESS","ORGANIZER","'"+name + "','" + mail + "','" + address+"'")
	return result

########################
# 
# ORGANIZER_LOGIN
#
########################

def add_organizer_login(org_id,username,password):
	result = insert("USERNAME,PASSWORD,ORGANIZER_ID","ORGANIZER_LOGIN","'"+username + "','" + password + "'," + "CAST('"+str(org_id)+"' AS INTEGER) ")
	return result

def get_organizer_id_for_login(name,mail,address):
	others = "WHERE NAME=" + "CAST('"+str(name)+"' AS VARCHAR) " + "AND MAIL=" + "CAST('"+str(mail)+"' AS VARCHAR) " + "AND ADDRESS=" + "CAST('"+str(address)+"' AS VARCHAR) "
	result = select("ID","ORGANIZER",others)
	print("result in get org id:",result)
	return result[0][0]

@app.route('/api/organizer_login_verif',methods=['GET'])
def organizer_verify():
	username = request.form['username']
	password = request.form['password']
	others = "WHERE USERNAME=" + "CAST('"+str(username)+"' AS VARCHAR) " + "AND PASSWORD=" + "CAST('"+str(password)+"' AS VARCHAR) "
	result = select("*","ORGANIZER_LOGIN",others)
	if(type(result)==type([0,0])):
		found = {"result":1,"message" :"Login verified","org_id":result[0][2]}
		return found
	return result

########################
# 
# ORGANIZER_REVIEW
#
########################

def add_organizer_review(name,mail,address,username,password):
	return insert("NAME,MAIL,ADRESS,USERNAME,PASSWORD","ORGANIZER_REVIEW","'"+name + "','" + mail + "','" + address + "','" + username + "','" + password+"'")

@app.route('/api/admin/organizer_review',methods=['GET'])
def read_organizer_review():
	query = return_query()
	result = select("*","ORGANIZER_REVIEW")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"mail": row[2],
			"address": row[3],
			"username": row[4]
		})
	return jsonify(query)

@app.route('/api/organizer_approve/<org_id>',methods=['POST'])
def organizer_review_approve(org_id):
	others = "WHERE ID =" + "CAST('"+str(org_id)+"' AS INTEGER) "
	result = select("NAME,MAIL,ADDRESS,USERNAME,PASSWORD","ORGANIZER_REVIEW",others)
	print("result:",result)
	name = result[0][0]
	mail = result[0][1]
	address = result[0][2]
	username = result[0][3]
	password = result[0][4]
	org_result = add_organizer(name,mail,address)
	if(org_result['result'] != 1):
		return org_result
	f_result = add_organizer_login(get_organizer_id_for_login(name,mail,address),username,password)
	organizer_review_reject(org_id)
	return f_result

@app.route('/api/organizer_reject/<int:org_id>',methods=['DELETE'])
def organizer_review_reject(org_id):
	result = delete("ORGANIZER_REVIEW","ID="+"CAST('"+str(org_id)+"' AS INTEGER) ")
	return result

########################
# 
# EVENT
#
########################

@app.route('/api/events/<int:many>',methods=['GET'])
def read_events(many):
	print("IN READ EVENTSSS")
	print("read event")
	print(type(many))
	query = return_query()
	date = datetime.now().date()
	others = others = """WHERE TIME  >= """ +"CAST('"+str(date)+"""'AS DATE)
		ORDER BY TIME ASC
		LIMIT """ + "CAST('"+str(many)+"'AS INTEGER)"

	result = select("ID,NAME,CITY,LOCATION,TIME,TYPE,IMAGE","EVENT",others)
	print(result)
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		print(row)
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"image": row[6],
		})
	return jsonify(query)

@app.route('/api/org_events/<int:org_id>',methods=['GET'])
def read_organizers_events(org_id):
	query = return_query()
	date = datetime.now().date()
	result = select("*","EVENT","WHERE ORGANIZER_ID = " +"CAST('"+str(org_id)+"' AS INTEGER)"+ """
		AND TIME >= """ +"CAST('"+str(date)+"""'AS DATE)
		ORDER BY TIME ASC""")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"description": row[6],
			"image": row[7],
			"url": row[8],
			"org_id": row[9]
		})
	return jsonify(query)

@app.route('/api/event_detail/<int:e_id>',methods=['GET'])
def read_event(e_id):
	print("IN READ EVENT")
	query = return_query()
	row = select("*","EVENT","WHERE ID = " +"CAST('"+str(e_id)+"' AS INTEGER)")
	if(type(row)!= type([1,1])):
		return row
	row = row[0]
	query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"description": row[6],
			"image": row[7],
			"url": row[8],
			"org_id": row[9]
		})
	return jsonify(query)

def add_event(name,city,location,date,e_type,ticket_url,image="",description="",org_id=None):
	others = "WHERE NAME='"+name+"' AND CITY='"+city+"' AND LOCATION='"+location+"' AND TIME="+"CAST('"+ str(date)+"' AS DATE)"+" AND TYPE='"+e_type+"' AND URL='"+ticket_url+"'"
	if(org_id!=None):
		others += " AND ORGANIZER_ID="+ "CAST('"+ str(org_id)+"' AS INTEGER) "
	if(image!=""):
		others += " AND IMAGE='"+image+"'"
	if(description!=""):
		others += " AND DESCRIPTION='"+description+"'"
	duplicate = select("*","EVENT",others)
	if(type(duplicate)==type([0,0])):
		print("\n\nDUPLICATE ALERT\n")
		return {"result":-1,"message":"duplicated"}
	print("not duplicate")
	values = "'"+name+"','"+city+"','"+location+"',"+"CAST('"+ str(date)+"' AS DATE) "+",'"+e_type+"','"+description+"','"+image+"','"+ticket_url+"'"
	#print("IN ADD EVENT values:",values)
	if(org_id == None):
		result =insert("NAME,CITY,LOCATION,TIME,TYPE,DESCRIPTION,IMAGE,URL","EVENT",values)
	else:
		values = values + ",CAST('"+ str(org_id)+"' AS INTEGER) "
		result = insert("NAME,CITY,LOCATION,TIME,TYPE,DESCRIPTION,IMAGE,URL,ORGANIZER_ID","EVENT",values)
	return result


def delete_event(e_id):
	return delete("EVENT","ID ="+"CAST('"+ str(e_id)+"' AS INTEGER) ")

@app.route('/api/filterby_city/<city>',methods=['GET'])
def filter_by_city(city):
	query = return_query()
	result = select("*","EVENT","WHERE CITY= '"+ city +"'")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"image": row[7]
		})
	return jsonify(query)

@app.route('/api/filterby_type/<e_type>',methods=['GET'])
def filter_by_type(e_type):
	query = return_query()
	result = select("*","EVENT","WHERE TYPE= '"+ e_type +"'")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"image": row[7]
		})
	return jsonify(query)

@app.route('/api/search/<keyword>',methods=['GET'])
def search_by_keyword(keyword):
	query = return_query()
	result = search(keyword)
	print("result:",result)
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"image": row[7]
		})
	return jsonify(query)
	
########################
# 
# EVENT REVIEW
#
########################

@app.route('/api/admin/event_review',methods=['GET'])
def read_event_review():
	query = return_query()
	result = select("*","EVENT_REVIEW")
	if(type(result)!= type([1,1])):
		return result
	for row in result:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"type": row[5],
			"description": row[6],
			"image": row[7],
			"ticket_url": row[8],
			"org_id": row[9],
			"old_id": row[10]
		})
	return jsonify(query)

def add_event_review(name,city,location,date,e_type,org_id,ticket_url="",description="",image="",old_evet_id=None):
	if(old_evet_id == None):
		values = "'" + name + "','" + city + "','" +location + "'," + "CAST('"+str(date)+"' AS DATE)" + ",'" +e_type + "','" + description + "','" +image + "','" +ticket_url +"',CAST('"+ str(org_id)+"' AS INTEGER) "
		result = insert("NAME,CITY,LOCATION,TIME,TYPE,DESCRIPTION,IMAGE,URL,ORGANIZER_ID","EVENT_REVIEW",values)
	else:
		values = "'" + name + "','" + city + "','" +location + "'," + "CAST('"+str(date)+"' AS DATE)" + ",'" +e_type + "','" + description + "','" +image + "','" +ticket_url +"',CAST('"+ str(org_id)+"' AS INTEGER) " + ",CAST('"+ str(old_evet_id)+"' AS INTEGER) "
		result = insert("NAME,CITY,LOCATION,TIME,TYPE,DESCRIPTION,IMAGE,URL,ORGANIZER_ID,OLD_EVENT_ID","EVENT_REVIEW",values)
	return result

@app.route('/api/add_new_event/<int:org_id>',methods=['POST'])
def new_event(org_id):
	name = request.form['name']
	city = request.form['city']
	location = request.form['location']
	date = request.form['date']
	e_type = request.form['type']
	description = request.form['description']
	image = request.form['image']
	ticket_url = request.form['ticket_url']
	return add_event_review(name,city,location,date,e_type,org_id,description,image,ticket_url)

@app.route('/api/event_update',methods=['POST'])
def update_event():
	old_evet_id = request.args.get('old_event_id')
	org_id = request.args.get('org_id')
	name = request.form['name']
	city = request.form['city']
	location = request.form['location']
	date = request.form['date']
	e_type = request.form['type']
	description = request.form['description']
	image = request.form['image']
	ticket_url = request.form['ticket_url']
	return add_event_review(name,city,location,date,e_type,org_id,description,image,ticket_url,old_evet_id)

@app.route('/api/new_event_approve/<int:e_id>',methods=['POST'])
def new_event_review_approve(e_id):
	result = select("*","EVENT_REVIEW","WHERE ID="+"CAST('"+str(e_id)+"' AS INTEGER) ")
	result = result[0]
	name = result[1]
	city = result[2]
	location = result[3]
	date = result[4]
	e_type = result[5]
	ticket_url = result[6]
	description = result[7]
	image = result[8]
	org_id = result[9]
	result = add_event(name,city,location,date,e_type,ticket_url,description,image,org_id)
	deleted = event_review_reject(e_id)
	return result

@app.route('/api/updated_event_approve/<int:e_id>',methods=['PUT'])
def updated_event_review_approve(e_id):
	result = select("*","EVENT_REVIEW","WHERE ID="+"CAST('"+str(e_id)+"' AS INTEGER) ")
	result = result[0]
	name = result[1]
	city = result[2]
	location = result[3]
	date = result[4]
	e_type = result[5]
	ticket_url = result[6]
	description = result[7]
	image = result[8]
	org_id = result[9]
	old_e_id = result[10]
	columns_values = "NAME='"+ name + "',CITY='"+ city + "',LOCATION='" + location+"',TIME="+"CAST('"+str(date)+"' AS DATE)"+ ",TYPE='"+e_type+"',DESCRIPTION='"+description+"',IMAGE='"+image+"',URL='"+ticket_url+"'"
	result = update("EVENT",columns_values,"ID="+"CAST('"+str(old_e_id)+"' AS INTEGER) ")
	event_review_reject(e_id)
	return result

@app.route('/api/event_reject/<int:e_id>',methods=['DELETE'])
def event_review_reject(e_id):
	result = delete("EVENT_REVIEW","ID="+"CAST('"+str(e_id)+"' AS INTEGER) ")
	return result
########################
# 
# USERNAME USAGE 
#
########################

@app.route('/api/username_control/<username>',methods=['GET'])
def username_verif(username):
	result = select("*","ORGANIZER_LOGIN","WHERE USERNAME='"+username+"'")
	if(type(result)== type([0,0])):
		result = {"result":-1,"message": "Username has already been in use"}
		return result
	else:
		result = select("*","ORGANIZER_REVIEW","WHERE USERNAME='"+username+"'")
		if(type(result)== type([0,0])):
			result = {"result":-1,"message": "Username has already been in use"}
			return result
		else:
			return {"result":1,"message":"Username can be used"}


def add_scrapped(myjson):
	print("__add scrapped called__")
	print(myjson)
	print("NAME:",myjson["name"])
	print("DATE:",myjson["date"])
	query = add_event(myjson["name"],myjson["city"],myjson["location"],myjson["date"],myjson["url"],myjson["description"],myjson["image"])
	print("scrapped",query)
	return 0



@app.route("/")
def home_page():
	query = return_query()
	for i in range(10):
		query.add(i,{
			'key':i,
			'value':i*24
		})
		madate = datetime.now() - timedelta(days = 0)
		queryXDV = add_organizer("xfbxdbxf","sfas@ryr.dgs","street lush NY")
	add_event_review("SOETHING","FORJT","CRR",madate,"MUSIC",47,"sgs.hf.com","snkfnsklfleksmglkemlk","sfa.jpg") 
	#print(select("*","EVENT"))
	return "efe"


if(DEBUG == True):
	os.environ['DATABASE_URL'] = "dbname='upcoming-events-platform' user='postgres' host='localhost' password='softeng2019'"
	initialize(os.environ.get('DATABASE_URL'))
if __name__ == "__main__":
	if(DEBUG):
		app.run(debug='True')
	else:
		app.run()