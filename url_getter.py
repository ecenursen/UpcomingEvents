import os,sys
import psycopg2 as db

DEBUG = False
def give_url():
    if(DEBUG == False):
	    return os.getenv("DATABASE_URL")
    else:
        return "dbname='upcoming-events-platform' user='postgres' host='localhost' password='softeng2019'"
        
def give_debug_status():
    return DEBUG