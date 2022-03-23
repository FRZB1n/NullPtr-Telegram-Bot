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
    if check_ban(message):
        return
    f.start(bot, message)


@bot.message_handler(content_types=['text'])
def txt_handler(message: types.Message):
    if check_ban(message):
        return

    status = f.check_status(message)

    if message.text == 'Subscription':
        f.subscription(bot, message)

    elif message.text == 'HWID del':       
        if status > 0:
            f.hwid_res_start(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")
            
    elif message.text == 'Ban':
        if status > 1:
            f.ban_start(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")
    
    elif message.text == 'Unban':
        if status > 1:
            f.unban_start(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")
        



def check_ban(message: types.Message):
    connect = sqlite3.connect('users.db')
    cur = connect.cursor()

    cur.execute(f"SELECT ban FROM records WHERE user_id = {message.chat.id}")
    ban = cur.fetchone()
    if ban[0] == True:
        video = open('videoplayback.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        return True

    return False

bot.polling()