import sqlite3

conn = sqlite3.connect("DB.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS login (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'police', 'admin'))
);
""")
cur.execute("SELECT * FROM login WHERE username='admin'")
if cur.fetchone() is None:
    cur.execute("INSERT INTO login VALUES (?, ?, ?, ?)", ('admin', 'admin', 'Administrator', 'admin'))

cur.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    complaint_text TEXT NOT NULL,
    status TEXT DEFAULT 'Submitted',
    date TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS criminals (
    criminal_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    crime TEXT,
    status TEXT
);
""")

conn.commit()
conn.close()
print("Database initialized.")