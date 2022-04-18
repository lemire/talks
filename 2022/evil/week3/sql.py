import sqlite3

from datetime import datetime


con = sqlite3.connect("img.db")
with con:
    tables = [row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    if not "geo" in tables:
        con.execute("CREATE TABLE geo (date TEXT, long NUMERIC, lat NUMERIC)")
    for row in  con.execute("SELECT * FROM geo"):
        print(row)
    dt = datetime.now()
    con.execute("INSERT INTO geo (date,long,lat) values (\""+str(dt)+"\",0.12323, 12.222) ")
con.close()

