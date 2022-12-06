import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')