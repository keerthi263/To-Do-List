import sqlite3

conn = sqlite3.connect(r"C:\Users\ELCOT\Desktop\python projects\todo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todo (
id INTEGER PRIMARY KEY AUTOINCREMENT,
task TEXT
)
""")

conn.commit()
conn.close()