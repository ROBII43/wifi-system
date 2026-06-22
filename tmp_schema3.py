import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
print('DB', os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_NAME'))
conn = mysql.connector.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'), connection_timeout=5)
cur = conn.cursor()
cur.execute('SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ORDINAL_POSITION', (os.getenv('DB_NAME'), 'transactions'))
print('COLUMNS', cur.fetchall())
cur.execute('SELECT COUNT(*) FROM transactions')
print('ROWS', cur.fetchone())
cur.close()
conn.close()
