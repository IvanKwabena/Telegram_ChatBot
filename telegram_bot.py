# Packages
# from Settings.config import MONGODB_KEY
from chats import TeleChats
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
# print(os.getenv('PATH'))

TELE_KEY = os.getenv("TELEGRAM_API_KEY")
# print(TELE_KEY)
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
        db.insert_one({'id':dic_user['id'], 'events':{name:date}})
    else :
        dic_events = db.find_one({'id':dic_user['id']})['events']
        dic_events.update({name:date})
        db.update_one({'id':dic_user['id']},  {"$set":{"events":dic_events}})

    msg =  name+": "+date+" saved."
    bot.send_message(message.chat.id, msg)


## Check
@bot.message_handler(commands=['check'])
def _check(message):
    dic_user["id"] = str(message.chat.id) 

    ## error
    lst_users = db.distinct(key="id")
    if dic_user["id"] not in lst_users:
        msg = "First you need to save an event with \n/save"

    ## query
    else:
        dic_events = db.find_one({"id":dic_user["id"]})["events"]
        today = datetime.datetime.today().strftime('%b %d')
        logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- CHECKING")
        res = [k for k,v in dic_events.items() if v == today]
        msg = "Today's events: "+", ".join(res) if len(res) > 0 else "No events today"
    
    bot.send_message(message.chat.id, msg)



# /view
@bot.message_handler(commands=['view'])
def _view(message):
    dic_user["id"] = str(message.chat.id) 

    ## error
    lst_users = db.distinct(key="id")
    if dic_user["id"] not in lst_users:
        msg = "You have no events. Save an event with \n/save"

    ## query
    else:
        dic_events = db.find_one({"id":dic_user["id"]})["events"]
        dic_events_sorted = {k:v for k,v in sorted(dic_events.items(), key=lambda item:item[0])}
        logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- VIEW ALL")
        msg = "\n".join(k+": "+v for k,v in dic_events_sorted.items())
    
    bot.send_message(message.chat.id, msg)


#delete
@bot.message_handler(commands=['delete'])
def _delete(message):
    msg = "Tell me the event to Delete, for example: \n\
        xmas day \nAnd I'm gonna stop the reminder."
    message = bot.reply_to(message, msg)
    bot.register_next_step_handler(message, delete_event)

def delete_event(message):
    dic_user['id'] = str(message.chat.id)

    txt = message.text
    logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- DELETE - "+txt)

    ## delete
    dic_events = db.find_one({'id': dic_user['id']})['events']
    dic_events.pop(txt)
    db.update_one({'id':dic_user['id']},  {"$set":{"events":dic_events}})

    # send done
    msg =  txt+" deleted."
    bot.send_message(message.chat.id, msg)


# non command message 
@bot.message_handler()
def temp(message):
    msg =TeleChats(message).bot_chat()
# def chat(message):
    # txt = message.text
    # if any(x in txt.lower() for x in ["thank","thx","cool"]):
    #     msg = "anytime"
    # elif any(x in txt.lower() for x in ["hi","hello","yo","hey"]):
    #     msg = "yo" if str(message.chat.username) == "none" else "yo "+str(message.chat.username)
    # else:
    #     msg = "save a date with \n/save"

    bot.send_message(message.chat.id, msg)

def scheduler():
    lst_users = db.distinct(key='id')
    logging.info("--- SCHEDULER for "+str(len(lst_users))+" users ---")
    for user in lst_users:
        dic_events = db.find_one({'id':dic_user['id']})['events']
        today = datetime.datetime.today().strftime('%b %d')
        res = [k for k, v in dic_events.items() if v == today]
        if len(res) > 0:
            msg = "Today's events: "+", ".join(res)
            bot.send_message(user, msg)




# bot.polling(none_stop=True)
import flask
from flask import  request
import threading

app = flask.Flask(__name__)

@app.route('/'+TELE_KEY, methods=['GET'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegrambot2116.herokuapp.com/'+TELE_KEY )
    return 200

if __name__ == "__main__":
    # print("---", datetime.datetime.now().strftime("%H:%M"), "---")
    # if datetime.datetime.now().strftime("%H:%M") in ["05:00","05:01","06:00","06:01","07:00","07:01"]:
    #     threading.Thread(target=scheduler).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)

