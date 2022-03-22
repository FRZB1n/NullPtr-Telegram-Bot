from email import message
from telebot import types
import telebot
from func import Work
import sqlite3

adm= [
    '1030297121',# FRZ
    '630035056'#HOHOL
]




bot = telebot.TeleBot("5111501194:AAGt_2JJPpvPbT6846bPQj83GhWB7Ju3720")
f = Work()
@bot.message_handler(commands=['start'])
def init(message):
    f.start(bot, message)


@bot.message_handler(content_types=['text'])
def txt_handler(message: types.Message):
  if message.text == 'Subscription':
    f.subscription(bot, message)




bot.polling()