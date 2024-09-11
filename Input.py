from databaseURL import Host, DBname, User, Password, Port
import psycopg2
import csv
import time

conn = psycopg2.connect(host = Host, dbname = DBname, user = User, password = Password, port = Port)
cur = conn.cursor()

def empty_string_to_none(value):
    return None if value == '' else value

with open('Book.csv', 'r', encoding='utf-8') as f:
    print("================================================= Book.csv =================================================")
    time.sleep(5)
    cnt = 1
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        row = [empty_string_to_none(value) for value in row]  # Convert empty strings to None
        cur.execute(
        "INSERT INTO \"Book\" (\"bookId\", \"callNum1\", \"callNum2\", \"bookName\", \"writer\", \"published\") VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (\"bookId\", \"bookName\") DO NOTHING",
        row
        )
        cnt += 1
        print(f"Book: {cnt}")

with open('Exist.csv', 'r', encoding='utf-8') as f:
    print("================================================= Exist.csv =================================================")
    time.sleep(5)
    cnt = 1
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        row = [empty_string_to_none(value) for value in row]  # Convert empty strings to None
        cur.execute(
        "INSERT INTO \"Exist\" (\"bookId\", \"libId\") VALUES (%s, %s) ON CONFLICT (\"bookId\", \"libId\") DO NOTHING",
        row
        )
        cnt += 1
        print(f"Exist: {cnt}")

with open('Lib.csv', 'r', encoding='EUC-KR') as f:
    print("================================================= Lib.csv =================================================")
    time.sleep(5)
    cnt = 1
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        row = [empty_string_to_none(value) for value in row]  # Convert empty strings to None
        cur.execute(
        "INSERT INTO \"Library\" (\"libId\", \"libName\", \"latitude\", \"longitude\", \"open\") VALUES (%s, %s, %s, %s, %s) ON CONFLICT (\"libId\") DO NOTHING",
        row
        )
        cnt += 1
        print(f"Library: {cnt}")


conn.commit()