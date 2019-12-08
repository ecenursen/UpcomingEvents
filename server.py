import os,sys
from flask import Flask
from dbinit import initialize


app = Flask(__name__)
app.config['SECRET_KEY'] = ''

DEBUG = False
if(DEBUG == False):
	url = os.getenv("DATABASE_URL")
else:
    url = "dbname='upcoming-events-platform' user='postgres' host='localhost' password='softeng2019'"
    initialize(url)
	# drop_table(url)


@app.route("/")
def home_page():
    return "UPCOMING EVENTS PLATFORM!"


if __name__ == "__main__":
    if(DEBUG):
		app.run(debug='True')
	else:
		app.run()

