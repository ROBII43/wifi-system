import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
print('before conn', flush=True)
conn = mysql.connector.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'), connection_timeout=5)
print('after conn', flush=True)
cur = conn.cursor()
print('before show tables', flush=True)
cur.execute('SHOW TABLES')
print('after show tables', flush=True)
print('tables:', cur.fetchall(), flush=True)
print('before schema', flush=True)
cur.execute('SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema=%s AND table_name=%s', (os.getenv('DB_NAME'),'transactions'))
print('after schema', flush=True)
print(cur.fetchall(), flush=True)
conn.close()
print('done', flush=True)
