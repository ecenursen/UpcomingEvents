import os,sys
from flask import Flask, jsonify, request
from dbinit import initialize,drop_table
import psycopg2 as db
import json
from datetime import datetime,timedelta
from url_getter import *
from db_cursor import select,insert,update,delete


class return_query(dict):
	def __init__ (self):
		self = dict()
	def add(self,key,value):
		self[key] = value

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

def add_admin(username,password):
	result = insert("ADMIN","USERNAME,PASSWORD","CAST("+str(username)+" AS VARCHAR)""" + """,
			""" +"CAST('"+ str(password)+"' AS VARCHAR) """)
	return result
	

def add_event_review(name,city,location,date,ticket_url,text,image,org_id):
	message = {}
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """INSERT INTO EVENT (NAME,CITY,LOCATION,TIME,TEXT,IMAGE,URL,ORGANIZER_ID) VALUES (
			""" +"CAST('"+str(name)+"' AS VARCHAR)" + """,
			""" +"CAST('"+ str(city)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(location)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+str(date)+"' AS DATE)""" + """,
			""" +"CAST('"+str(text)+" 'AS VARCHAR)""" + """,
			""" +"CAST('"+ str(image)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(ticket_url)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(org_id)+"' AS INTEGER) """ + """
		);
		"""
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	message["result"] = 1
	message["message"] = "add_event_review success"
	json_message = json.dumps(message)
	return json_message

def add_organizer_review(name,mail,address,username,password):
	message = {}
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """INSERT INTO ORGANIZER_REVIEW (NAME,MAIL,ADDRESS,USERNAME,PASSWORD) VALUES (
			""" +"CAST("+str(name)+" AS VARCHAR)""" + """,
			""" +"CAST('"+ str(mail)+"' AS VARCHAR) """ + """,
			""" +"CAST("+str(address)+" AS VARCHAR)""" + """,
			""" +"CAST("+str(username)+" AS VARCHAR)""" + """,
			""" +"CAST('"+ str(password)+"' AS VARCHAR) """ + """
		);
		"""
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	message["result"] = 1
	message["message"] = "add_organizer_review success"
	json_message = json.dumps(message)
	return json_message

def add_organizer(name,mail,address):
	message = {}
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """INSERT INTO ORGANIZER (NAME,MAIL,ADDRESS) VALUES (
			""" +"CAST('"+str(name)+"' AS VARCHAR)""" + """,
			""" +"CAST('"+ str(mail)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+str(address)+"' AS VARCHAR)""" + """
		);
		"""
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	message["result"] = 1
	message["message"] = "add_organizer success"
	json_message = json.dumps(message)
	return json_message

def add_organizer_login(org_id,username,password):
	message = {}
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """INSERT INTO ORGANIZER_LOGIN(USERNAME,PASSWORD,ORGANIZER_ID) VALUES (
			""" +"CAST('"+str(username)+"' AS VARCHAR)""" + """,
			""" +"CAST('"+ str(password)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+str(org_id)+"' AS INTEGER)""" + """
		);
		"""
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	message["result"] = 1
	message["message"] = "add_organizer_login success"
	json_message = json.dumps(message)
	return json_message

@app.route('/api/event/',methods=['POST'])
def create_event():
	name = request.form['name']
	city = request.form['city']
	location = request.form['location']
	date = request.form['date']
	text = request.form['text']
	image = request.form['image']
	ticket_url = request.form['url']
	org_id = request.form['org_id']
	return add_event(name,city,location,date,text,image,ticket_url,org_id)

def add_scrapped(myjson):
	query = add_event(myjson["name"],myjson["city"],myjson["location"],myjson["date"],myjson["url"],myjson["text"],myjson["image"])
	print("scrapped",query)
	return 0

def add_event(name,city,location,date,ticket_url,text="",image="",org_id=""):
	if(org_id == ""):
		result =insert("EVENT","NAME,CITY,LOCATION,TIME,TEXT,IMAGE,URL","CAST('"+str(name)+"' AS VARCHAR)" + """,
			""" +"CAST('"+ str(city)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(location)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+str(date)+"' AS DATE)""" + """,
			""" +"CAST('"+str(text)+"' AS VARCHAR)""" + """,
			""" +"CAST('"+ str(image)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(ticket_url)+"' AS VARCHAR) """)
	else:
		result = insert("EVENT","NAME,CITY,LOCATION,TIME,TEXT,IMAGE,URL,ORGANIZER_ID","CAST('"+str(name)+"' AS VARCHAR)" + """,
			""" +"CAST('"+ str(city)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(location)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+str(date)+"' AS DATE)""" + """,
			""" +"CAST('"+str(text)+"' AS VARCHAR)""" + """,
			""" +"CAST('"+ str(image)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(ticket_url)+"' AS VARCHAR) """ + """,
			""" +"CAST('"+ str(org_id)+"' AS INTEGER) """)
	print("ADD EVENT:",result)
	return result

@app.route('/api/event_review',methods=['GET'])
def read_event_review():
	print("read event review")
	query = return_query()
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """ SELECT * FROM EVENT_REVIEW
		ORDER BY TIME ASC"""
	cursor.execute(statement)
	connection.commit()
	for row in cursor:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"text": row[5],
			"image": row[6],
			"url": row[7],
			"org_id": row[8]
		})
	cursor.close()
	return jsonify(query)

@app.route('/api/organizer_review',methods=['GET'])
def read_organizer_review():
	print("read organizer review")
	query = return_query()
	connection = db.connect(url)
	cursor = connection.cursor()
	statement = """SELECT * FROM ORGANIZER_REVIEW"""
	cursor.execute(statement)
	connection.commit()
	for row in cursor:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"mail": row[2],
			"adress": row[3]
		})
	cursor.close()
	return jsonify(query)

@app.route('/api/events/<int:many>',methods=['GET'])
def read_event(many):
	print("read event")
	print(type(many))
	query = return_query()
	connection = db.connect(url)
	cursor = connection.cursor()
	date = datetime.now().date()
	statement = """ SELECT * FROM EVENT
		WHERE TIME  >= """ +"CAST('"+str(date)+"""'AS DATE)
		ORDER BY TIME ASC
		LIMIT """ + "CAST('"+str(many)+"'AS INTEGER)"
	cursor.execute(statement)
	connection.commit()
	for row in cursor:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"text": row[5],
			"image": row[6],
			"url": row[7],
			"org_id": row[8]
		})
	cursor.close()
	return jsonify(query)

def read_organizers_event(org_id):
	print("read ORGANIZERS' event")
	query = return_query()
	connection = db.connect(url)
	cursor = connection.cursor()
	date = datetime.now().date()
	statement = """ SELECT * FROM EVENT
		WHERE ORGANIZER_ID = """ +"CAST('"+str(org_id)+"' AS INTEGER)"+ """
		AND TIME >= """ +"CAST('"+str(date)+"""'AS DATE)
		ORDER BY TIME ASC"""
	cursor.execute(statement)
	connection.commit()
	for row in cursor:
		query.add(row[0],{
			"id": row[0],
			"name": row[1],
			"city": row[2],
			"location": row[3],
			"date": row[4],
			"text": row[5],
			"image": row[6],
			"url": row[7],
			"org_id": row[8]
		})
	cursor.close()
	return jsonify(query)



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
		add_event("hobaa","NY","MAGNOLIA PUDDING",madate.date(),"http.sdgsg.com","jjnjn","sdfsd.jpg") 
	return read_event(1000)

if __name__ == "__main__":
	if(give_debug_status):
		initialize(give_url)
		app.run(debug='True')
	else:
		app.run()
