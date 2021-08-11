# # Packages
# import telebot
# import dateparser
# import datetime
# import logging
# import pymongo
# from Settings import config

# ## bot 
# bot = telebot.TeleBot(token='1927260097:AAG6DlpvxltSh2Totp3dzpRdh0efTkb4LDA')
# dic_user = {}

# ## setup db
# client = pymongo.MongoClient(config.mongodb_keys)
# db_name = 'Telegram_bot'
# collection_name = 'users'
# db = [db_name][collection_name]
# ''
# ## logging 
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)


# # /start
# @bot.message_handler(commands=['start'])
# def _start(message):
#     ## reset
#     dic_user["id"] = str(message.chat.id)
#     db.delete_one({'id':dic_user["id"]})
#     logging.info(str(message.chat.username)+" - "+str(message.chat.id)+" --- START")

#     ## send first msg
#     msg = "Hello "
#     # +str(message.chat.username)+\
#         #   ", I'm a date reminder. Tell me birthdays and events to remind you. To learn how to use me, use \n/help"
#     bot.send_message(message.chat.id, msg)


# bot.polling()

# # # run
# # if config.ENV == "DEV":
# #     bot.infinity_polling(True)  #bot.polling()


# import os
# from dotenv import load_dotenv
# load_dotenv()

# Telegram = os.getenv(API_Key)




