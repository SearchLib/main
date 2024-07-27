__package__ = "main"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databaseURL import Host, DBname, User, Password, Port
import psycopg2

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host = Host, dbname = DBname, user = User, password = Password, port = Port)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()