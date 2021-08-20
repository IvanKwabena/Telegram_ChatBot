
import telebot
import os


TELE_KEY = os.getenv("TELEGRAM_API_KEY")
bot = telebot.TeleBot(TELE_KEY)

class TeleChats:

    def __init__(self, message):
        self.message = message


    def bot_chat(self):
        txt = self.message.text
        msg = ''
        if any(x in txt.lower() for x in ["thank","thx","cool"]):
            msg = "anytime"
        elif any(x in txt.lower() for x in ["hi","hello","yo","hey"]):
            msg = "yo" if str(self.message.chat.username) == "none" else "yo "+str(self.message.chat.username)
        else:
            msg = "save a date with \n/save"
        return msg
