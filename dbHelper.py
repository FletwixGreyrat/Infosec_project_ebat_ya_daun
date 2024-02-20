import sqlite3

db = sqlite3.connect("data.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS intermediate (userId TEXT, request TEXT)""")

# db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS global(userId TEXT, answer TEXT)""")
# db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS cloud(
fileId TEXT,
dataType TEXT
)""")
db.commit()