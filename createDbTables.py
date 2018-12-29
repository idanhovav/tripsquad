import sqlite3 as s

db_path = "main.db"

conn = s.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE accounts (uid TEXT PRIMARY KEY, timeCreated TEXT, name TEXT, email TEXT UNIQUE, passwordHash TEXT)''')
c.execute('''CREATE TABLE trips (uid TEXT PRIMARY KEY, timeCreated TEXT, creatorAccountID FOREIGN KEY, name TEXT, description TEXT)''')
c.execute('''CREATE TABLE trip_members (uid TEXT PRIMARY KEY, accountID FOREIGN KEY, tripID FOREIGN KEY, totalPurchaseAmt INTEGER)''')
c.execute('''CREATE TABLE purchases (uid TEXT PRIMARY KEY, tripMemberID FOREIGN KEY, tripID FOREIGN KEY, purchaseAmt INTEGER, timeCreated TEXT, description TEXT)''')


def db_add_post(text, xCoordinate, yCoordinate):
	conn = s.connect(db_path)
	c = conn.cursor()
	assert isinstance(text, str), "text must be a string."
	assert isinstance(xCoordinate, int), "xCoordinate must be a string."
	assert isinstance(yCoordinate, int), "yCoordinate must be a string."
	postInfo = (text, xCoordinate, yCoordinate)
	# this is safe
	c.execute("INSERT INTO posts VALUES (?, ?, ?)", postInfo)
	conn.commit()

@app.teardown_appcontext
def close_connection(exception):
	conn = s.connect(db_path)
	conn.close()

def db_get_posts():
	conn = s.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT * FROM posts")
	return c.fetchall()

c.execute("INSERT INTO meals VALUES (?, ?, ?)", info)
