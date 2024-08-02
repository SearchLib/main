__package__ = "main"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
from databaseURL import Host, DBname, User, Password, Port
import psycopg2

Base = registry().generate_base()
engine = create_engine(f"postgresql://{User}:{Password}@{Host}:{Port}/{DBname}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host = Host, dbname = DBname, user = User, password = Password, port = Port)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()