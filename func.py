import telebot
from telebot import types
import sqlite3
import datetime

user_kb = telebot.types.ReplyKeyboardMarkup(True)
user_kb.row('Buy', 'Change password', 'Subscription')

adm_kb = telebot.types.ReplyKeyboardMarkup(True)
adm_kb.row('Ban', 'Unban', 'Give sub')
adm_kb.row('Give sub count',  'HWID del', 'Resller add')

res_kb = telebot.types.ReplyKeyboardMarkup(True)
res_kb.row('Give sub', 'HWID del', 'Get sub count')

class Work(object):
    def start(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            connect = sqlite3.connect('users.db')
            cur = connect.cursor()
            id = message.chat.id
            cur.execute("""CREATE TABLE IF NOT EXISTS records(
                user_id INTEGER NOT NULL,
                password CHAR,
                admin BOOL,
                reseller BOOL,
                reseller_sub_count INTEGER,
                hack_type CHAR,
                has_subscription BOOL,
                time_subscription DATE,
                hwid CHAR,
                ban BOOL
            )""")
            connect.commit()

            cur.execute(f"SELECT user_id FROM records WHERE user_id = {id}")
            data = cur.fetchone()

            
            if data is None:

                inf = [message.chat.id, False, False, 0, False, False]
                cur.execute("INSERT INTO records(user_id, admin, reseller,reseller_sub_count, has_subscription, ban) VALUES(?, ?,?,?,?,?);", inf)
                connect.commit()

                password = bot.send_message(message.chat.id, "Добро пожаловать, введите пароль, который будет исопльзоваться для дальнейшей авторизации")
                bot.register_next_step_handler (password, SetPass, bot)#atr
            else:
                cur.execute(f"SELECT ban FROM records WHERE user_id = {id}")
                ban = cur.fetchone()

                if ban[0] == True:
                    video = open('videoplayback.mp4', 'rb')
                    bot.send_video(message.chat.id, video)
                    return

                cur.execute(f"SELECT admin, reseller FROM records WHERE user_id = {id}")
                prev = cur.fetchone()
               
                if prev[0] == True:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= adm_kb)
                elif prev[1] == True:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= res_kb)
                else:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= user_kb)
                    
        except Exception as e:
            print(str(e))



    def subscription(self, bot: telebot.TeleBot ,message:types.Message):
        try:
           
            connect = sqlite3.connect('users.db')
            cur = connect.cursor()
            id = message.chat.id

            cur.execute(f"SELECT has_subscription FROM records WHERE user_id = {id}")
            has_sub = cur.fetchone()

            if has_sub[0] == True:

                #inf = [datetime.date.today(), id]   
                #cur.execute("UPDATE records SET time_subscription = ? WHERE user_id = ?", inf)
                #connect.commit()
                
                cur.execute(f"SELECT time_subscription FROM records WHERE user_id = {id}")
                date = cur.fetchone()
                Splitted = date[0].split("-")
                end_date = datetime.date(int(Splitted[0]), int(Splitted[1]), int(Splitted[2]))
            
                delta_date = end_date - datetime.date.today()

                bot.send_message(id, "Your subscription expiried at " + str(date[0]) + "\nDays left: " + str(delta_date.days))
            else:
                bot.send_message(id, "You haven't got any subscriptions yet")

            

        except Exception as e:
            print(str(e))


def SetPass(message:types.Message, bot: telebot.TeleBot):
    try:
        connect = sqlite3.connect('users.db')
        cur = connect.cursor()
        inf = [message.text, message.chat.id]   
        cur.execute(" UPDATE records SET password = ? WHERE user_id = ?", inf)
        connect.commit()

        cur.execute(f"SELECT admin, reseller FROM records WHERE user_id = {message.chat.id}")
        prev = cur.fetchone()
            
        if prev[0] == True:
            bot.send_message(inf[1], "Пароль успешно добавлен", reply_markup= adm_kb)
        elif prev[1] == True:
            bot.send_message(inf[1], "Пароль успешно добавлен", reply_markup= res_kb)
        else:
            bot.send_message(inf[1], "Пароль успешно добавлен", reply_markup= user_kb)

    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "Пароль не добавлен")