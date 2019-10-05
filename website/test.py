import sqlite3
import base64

conn = sqlite3.connect("../data")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM exo LIMIT 50")

def decode(data):
	return base64.b64decode(data[2:len(data)-1].encode("utf-8"))

data = []
for row in rows:
	tmp = [row[0], row[1], row[2], decode(row[3]), row[4], decode(row[5]), decode(row[6]), decode(row[7]), decode(row[8]), row[9], row[10], row[11]]
	data.append(tmp)