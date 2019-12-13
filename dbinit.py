import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [

    """CREATE TABLE IF NOT EXISTS ADMIN (
        USERNAME VARCHAR PRIMARY KEY,
        PASSWORD VARCHAR NOT NULL
        )""",

    
     """CREATE TABLE IF NOT EXISTS ORGANIZER (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        MAIL VARCHAR,
        ADDRESS VARCHAR
        )
    """,

    """CREATE TABLE IF NOT EXISTS EVENT_REVIEW (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        CITY VARCHAR(50) NOT NULL,
        LOCATION VARCHAR(50) NOT NULL,
        TIME DATE NOT NULL,
        TEXT VARCHAR,
        IMAGE VARCHAR,
        URL VARCHAR,
        ORGANIZER_ID INTEGER,
        FOREIGN KEY (ORGANIZER_ID) 
            REFERENCES ORGANIZER(ID)
            ON DELETE SET NULL
            ON UPDATE SET NULL
        )
    """,

    """CREATE TABLE IF NOT EXISTS ORGANIZER_REVIEW (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        MAIL VARCHAR,
        ADDRESS VARCHAR,
        USERNAME VARCHAR NOT NULL,
        PASSWORD VARCHAR NOT NULL
        )
    """,


    """CREATE TABLE IF NOT EXISTS ORGANIZER_LOGIN (
        USERNAME VARCHAR PRIMARY KEY,
        PASSWORD VARCHAR NOT NULL,
        ORGANIZER_ID INTEGER,
        FOREIGN KEY (ORGANIZER_ID) 
            REFERENCES ORGANIZER(ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )
    """,

    """CREATE TABLE IF NOT EXISTS EVENT (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        CITY VARCHAR(50) NOT NULL,
        LOCATION VARCHAR(50) NOT NULL,
        TIME DATE NOT NULL,
        TEXT VARCHAR,
        IMAGE VARCHAR,
        URL VARCHAR,
        ORGANIZER_ID INTEGER,
        FOREIGN KEY (ORGANIZER_ID) 
            REFERENCES ORGANIZER(ID)
            ON DELETE SET NULL
            ON UPDATE SET NULL
        )
    """
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

def drop_table(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("DROP SCHEMA public CASCADE;CREATE SCHEMA public;")
        cursor.close()