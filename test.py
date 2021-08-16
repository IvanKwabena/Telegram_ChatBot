# from Settings.config import TELEGRAM_KEY
# from Settings import config
# import os
# from dotenv import load_dotenv
# from pymongo import collection
# load_dotenv()
# from telegram import  bot
# # from telegram.ext import Updater, CommandHandler, CallbackContext
# import telebot
# import pymongo
# from pymongo import MongoClient

# env_path = os.path.join('D:\Programming\Flutter\Extras\Bot_Telegram\Settings', 'D:\Programming\Flutter\Extras\Bot_Telegram\Settings\.env')
# load_dotenv(env_path)
# print(os.getenv('PATH'))
# os.environ['MON_KEY'] = 'mongodb+srv://Ivan:smoke..2116@mr-ivin.dpxot.mongodb.net/Telegram_bot?retryWrites=true&w=majority' 

# B_KEY = os.environ.get("MON_KEY")
# print(B_KEY)


# cluster = MongoClient('mongodb+srv://Ivan:smoke..2116@mr-ivin.dpxot.mongodb.net/Telegram_bot?retryWrites=true&w=majority')
# db = cluster['Telegram_bot']
# collection = db['users']

# post ={'_id':0, 'name':'Ivan', 'score':100}
# collection.insert_one(post)

# A_KEY = os.getenv("TELEGRAM_API_KEY")
# B_KEY = os.getenv("MONGODB_API_KEY")
# print(B_KEY)


# bot =telebot.TeleBot(A_KEY)
# print(bot)

# @bot.message_handler(commands=['start'])
# def greet(message):
#     bot.reply_to(message, "Hello")

# bot.polling(none_stop=True, timeout=123)
 # # run

# bot.infinity_polling()  #bot.polling()

# dev = config.envs




