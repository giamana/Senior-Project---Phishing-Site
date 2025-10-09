import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
if not os.path.exists(db_path):
    print(f"Database file not found: {db_path}")
    raise SystemExit(1)

con = sqlite3.connect(db_path)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cur.fetchall()
print('tables:', tables)
res = cur.execute('PRAGMA integrity_check;').fetchone()
print('integrity:', res[0] if res else None)
con.close()
