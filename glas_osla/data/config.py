import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = {871333900, 5251082575}
PGPASSWORD = os.getenv('dbPass')
DATABASE_NAME = os.getenv('db_name')
IP = os.getenv('ip')
PORT = os.getenv('port')

PG_URL = f'postgresql+asyncpg://postgres:{PGPASSWORD}@{IP}/{DATABASE_NAME}'
