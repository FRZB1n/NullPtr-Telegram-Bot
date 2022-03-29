from email import message
from telebot import types
import telebot
from func import Work, adm
import sqlite3





bot = telebot.TeleBot("5111501194:AAGt_2JJPpvPbT6846bPQj83GhWB7Ju3720")
f = Work()
@bot.message_handler(commands=['start'])
def init(message):
    if check_ban(message):
        return
    f.start(bot, message)


@bot.message_handler(commands=['help'])
def help(message):
    if check_ban(message):
        return
    f.help_init(bot, message)

@bot.message_handler(content_types=['text'])
def txt_handler(message: types.Message):
    if check_ban(message):
        return


    if f.CheckAcc(str(message.chat.id), adm):
        status = 3
    else:
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

    elif message.text == 'Give sub count':
        if status > 1:
            f.give_sub_count_start(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")

    elif message.text == 'Reseller add':
        if status > 1:
            f.resseler_add_init(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")

    elif message.text == 'Reseller del':
        if status > 1:
            f.resseler_del_init(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")

    elif message.text == 'Get sub count':
        if status > 0:
            f.get_sub_count(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")
    
    elif message.text == 'Give sub':
        if status > 0:
            f.give_sub_init(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")



def check_ban(message: types.Message):
    connect = sqlite3.connect('users.db')
    cur = connect.cursor()

    cur.execute(f"SELECT ban FROM records WHERE user_id = {message.chat.id}")
    ban = cur.fetchone()
    if ban is None:
        return

    if ban[0] == True:
        video = open('videoplayback.mp4', 'rb')
        bot.send_video(message.chat.id, video)
        return True

    return False

bot.polling()