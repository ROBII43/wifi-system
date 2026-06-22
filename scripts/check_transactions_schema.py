import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    connection_timeout=5,
)
cur = conn.cursor()
cur.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ORDINAL_POSITION", (os.getenv('DB_NAME'), 'transactions'))
columns = [row[0] for row in cur.fetchall()]
print('COLUMNS:', columns)
cur.execute('SELECT COUNT(*) FROM transactions')
print('TOTAL ROWS:', cur.fetchone()[0])
cur.execute('SELECT id, status, created_at FROM transactions ORDER BY created_at DESC LIMIT 20')
print('LATEST 20 TRANSACTIONS:')
for row in cur.fetchall():
    print(row)
conn.close()
