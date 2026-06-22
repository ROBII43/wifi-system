import os
from dotenv import load_dotenv
import mysql.connector
load_dotenv()
conn = mysql.connector.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'))
cur = conn.cursor()
cur.execute('SELECT id FROM transactions ORDER BY created_at DESC')
ids = [r[0] for r in cur.fetchall()]
print('TOTAL', len(ids))
for i in ids:
    print(i)
cur.close()
conn.close()
