import os

from dotenv import load_dotenv

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = {871333900, 5251082575}
PGUSER = os.getenv('username')
PGPASSWORD = os.getenv('dbPass')
DATABASE_NAME = os.getenv('db_name')
IP = os.getenv('ip')
PORT = os.getenv('port')

PG_URL = f'postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE_NAME}'
