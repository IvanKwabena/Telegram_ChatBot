import os
from dotenv import load_dotenv
load_dotenv()


ENV = 'PROD'

#keys
if ENV == 'PROD':
    TELEGRAM_KEY = os.getenv("TELEGRAM_API_KEY")
    MONGODB_KEY = os.getenv("MONGODB_API_KEY")

# elif ENV == 'PROD':
#     import ast
#     TELEGRAM_KEY = ast.literal_eval(os.getenv("TELEGRAM_API_KEY"))
#     MONGODB_KEY = ast.literal_eval(os.getenv("MONGODB_API_KEY"))

#server
host = '0.0.0.0'
port = int(os.environ.get("PORT", 5000))
webhook = 'https://bot-date-reminder.herokuapp.com/'

