from email import message
from telebot import types
import telebot
from func import Oplata, Work, adm
import sqlite3

from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime, PaymentMethods




bot = telebot.TeleBot("5111501194:AAGt_2JJPpvPbT6846bPQj83GhWB7Ju3720")
pay = Oplata()
f = Work()
@bot.message_handler(commands=['start'])
def init(message):
    f.download()
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
    elif message.text == 'fix prob':
        if status > 1:
            f.download()#ISSUE FIXED
            f.fixing_problems(bot, message)
        else:
            bot.send_message(message.chat.id, "You aren't accesible")

    elif message.text == 'fix prob':
       pay.init_pay(bot, message)
            


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.message:
        if call.data == "next":
            f.fixing_problems(bot, call.message)
        elif call.data == "stop":
            bot.send_message(call.message.chat.id, "Спасибо за помощь!")
        elif call.data == "apex":
            pay.apex_init(bot, call.message)
        elif call.data == "valorant":
            pay.valorant_init(bot, call.message)

        elif call.data == "day":
            pay.valorant_init(bot, call.message)
        elif call.data == "week":
            pay.valorant_init(bot, call.message)
        elif call.data == "month":
            pay.valorant_init(bot, call.message)
            


            

  


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