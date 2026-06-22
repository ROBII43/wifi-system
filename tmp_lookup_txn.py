import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
txn='TXN1780923332453KT198E'
print('Lookup', txn)
conn = mysql.connector.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'), connection_timeout=5)
cur = conn.cursor()
cur.execute('SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ORDINAL_POSITION', (os.getenv('DB_NAME'), 'transactions'))
cols = [r[0] for r in cur.fetchall()]
cur.execute('SELECT * FROM transactions WHERE id=%s LIMIT 1', (txn,))
row = cur.fetchone()
print('COLUMNS:', cols)
if row:
    print('FOUND:', row)
else:
    print('NOT FOUND')
cur.close()
conn.close()
