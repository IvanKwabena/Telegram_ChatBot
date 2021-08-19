# Packages
# from Settings.config import MONGODB_KEY
from pymongo import message
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
    db.delete_one({'id':dic_user["id"]})
    logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- START")

    ## send first msg
    msg = "Hello " +str(message.chat.username)+ ", I'm a Date reminder. Tell me birthdays and events to remind you. To learn how to use me, use \n/help"
    bot.send_message(message.chat.id, msg)


# /save
@bot.message_handler(commands=['save'])
def _save(message):
    msg = "Set an event in the format 'month dd', for example: \n\
        xmas day: Dec 25 \n\
I also understand: \n\
today, tomorrow, in 3 days, in 1 week, in 6 months, yesterday, 3 days ago ... so you can do: \n\
            meeting: tomorrow"
    message = bot.reply_to(message , msg)
    bot.register_next_step_handler(message, save_event)

def save_event(message):
    dic_user['id'] = str(message.chat.id)

    # get text
    txt = message.text
    logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- SAVE - "+txt)
    name , date = txt.split(':')[0], txt.split(':')[1] 

    ##check date
    date = dateparser.parse(date).strftime('%b %d')

    ##save
    lst_users = db.distinct(key='id')
    if dic_user['id'] not in lst_users:
        db.insert_one({'id':dic_user['id'], 'event':{name:date}})
    else :
        dic_events = db.find_one({'id':dic_user['id']})['events']
        dic_events.update({name:date})
        db.update_one({'id':dic_user['id']},  {"$set":{"events":dic_events}})

    msg =  name+": "+date+" saved."
    bot.send_message(message.chat.id, msg)


## Check
@bot.message_handler(commands=['check'])
def _check(message):
    dic_user['id'] = str(message.chat.id)

    #error
    lst_users = db.distinct(key='id')
    if dic_user not in lst_users:
        msg = "Please use the /save command to save an event first"
    
    #Query
    else :
        dic_events = db.find_one({'id': dic_user['id']})['events']
        today = datetime.datetime.today().strftime('%b %d')
        logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- CHECKING")
        res =  [k for k , v in dic_events.items() if v == 'today']
        msg = "Today's events: "+", ".join(res) if len(res) > 0 else "No events today"
    bot.send_message(message.chat.id, msg)



bot.polling(none_stop=True)


