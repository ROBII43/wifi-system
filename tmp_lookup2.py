import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
txn='TXN1780923332453KT198E'
print('LOOKUP', txn)
conn = mysql.connector.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'))
cur = conn.cursor()
cur.execute('SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema=%s AND table_name=%s ORDER BY ORDINAL_POSITION', (os.getenv('DB_NAME'), 'transactions'))
print('COLUMNS:', [r[0] for r in cur.fetchall()])
cur.execute('SELECT COUNT(*) FROM transactions')
print('TOTAL ROWS:', cur.fetchone()[0])
cur.execute('SELECT id, status, amount, phone, created_at, paid_at, active, expiry, mikrotik_status FROM transactions WHERE id=%s LIMIT 1', (txn,))
row = cur.fetchone()
if row:
    print('FOUND:', row)
else:
    print('NOT FOUND')
cur.close()
conn.close()
