# Packages
# from Settings.config import MONGODB_KEY
import telebot
import dateparser
import datetime
import logging
import pymongo
# from Settings import config
# from Settings.config import TELEGRAM_KEY
# from Settings import config
import os
from dotenv import load_dotenv
from pymongo import collection
load_dotenv()
from telegram import  bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from pymongo import MongoClient

## bot 

env_path = os.path.join('D:\Programming\Flutter\Extras\Bot_Telegram\Settings', 'D:\Programming\Flutter\Extras\Bot_Telegram\Settings\.env')
load_dotenv(env_path)
print(os.getenv('PATH'))

TELE_KEY = os.getenv("TELEGRAM_API_KEY")
print(TELE_KEY)
bot = telebot.TeleBot(TELE_KEY)
dic_user = {}

## setup db
MONGO_KEY = os.getenv("MONGODB_API_KEY")
print(MONGO_KEY)
client = pymongo.MongoClient(MONGO_KEY)
db_name = 'Telegram_bot'
collection_name = 'users'
db = client[db_name][collection_name]

## logging 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# /start
@bot.message_handler(commands=['start'])
def _start(message):
    ## reset
    dic_user["id"] = str(message.chat.id)
    db.insert_one({'id':dic_user["id"]})
    logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- START")

    ## send first msg
    msg = "Hello " +str(message.chat.username)+ ", I'm a Date reminder. Tell me birthdays and events to remind you. To learn how to use me, use \n/help"
    bot.send_message(message.chat.id, msg)

bot.polling(none_stop=True, timeout=123)


