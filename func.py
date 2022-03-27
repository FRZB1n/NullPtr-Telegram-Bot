import telebot
from telebot import types
import sqlite3
import datetime
import mysql.connector



adm= [
    '1030297121',# FRZ
    '630035056'#HOHOL
]


user_kb = telebot.types.ReplyKeyboardMarkup(True)
user_kb.row('Buy', 'Change password', 'Subscription')

adm_kb = telebot.types.ReplyKeyboardMarkup(True)
adm_kb.row('Ban', 'Unban', 'Give sub')
adm_kb.row('Give sub count',  'HWID del', 'Reseller add', 'Reseller del')

res_kb = telebot.types.ReplyKeyboardMarkup(True)
res_kb.row('Give sub', 'HWID del', 'Get sub count')
config = {
  'user': 'sql11481321',
  'password': 'XukZtZlx6b',
  'host': 'sql11.freemysqlhosting.net',
  'database': 'sql11481321'
}
class Work(object):
    def start(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()
            id = message.chat.id
            cur.execute("""CREATE TABLE IF NOT EXISTS records(
                user_id INTEGER NOT NULL,
                password TEXT,
                admin BOOL,
                reseller BOOL,
                reseller_sub_count INTEGER,
                hack_type TEXT,
                has_subscription BOOL,
                time_subscription DATE,
                hwid TEXT,
                ban BOOL
            )""")
            connect.commit()

            cur.execute(f"SELECT user_id FROM records WHERE user_id = {id}")
            data = cur.fetchone()


            if data is None:

               
                cur.execute(f"INSERT INTO records(user_id, admin, reseller,reseller_sub_count, has_subscription, ban) VALUES({int(message.chat.id)}, False, False, 0, False, False)")
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
               
                if self.CheckAcc(str(message.chat.id), adm):
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= adm_kb)
                elif prev[0] == True:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= adm_kb)
                elif prev[1] == True:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= res_kb)
                else:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= user_kb)
                
                cur.close()
                connect.close()
                    
        except Exception as e:
            print(str(e))

    def get_sub_count(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()
            id = message.chat.id
            cur.execute(f"SELECT reseller_sub_count FROM records WHERE user_id = {id}")
            res = cur.fetchone()
            bot.send_message(id, "Всего возможностей выдать подписок: " + str(res[0]))

        except Exception as e:
            print(str(e))


    def resseler_add_init(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя которому хотите выдать роль реселера")
            bot.register_next_step_handler (us_id, ressler_add, bot)
        except Exception as e:
            print(str(e))


    def resseler_del_init(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя у которого хотите отобрать роль реселера")
            bot.register_next_step_handler (us_id, ressler_del, bot)
        except Exception as e:
            print(str(e))

    def give_sub_count_start(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя которому хотите выдать возможность раздачи подписки")
            bot.register_next_step_handler (us_id, self.give_sub_count_int, bot)
        except Exception as e:
            print(str(e))

    def give_sub_count_int(self,message:types.Message, bot: telebot.TeleBot):
        try:
            
            sub_count = bot.send_message(message.chat.id, "Введите количество подписок возможных для выдачи юзером с id = " + str(message.text))
            bot.register_next_step_handler (sub_count, give_sub_count, bot, message.text)
            pass
        except Exception as e:
            print(str(e))
        
    def hwid_res_start(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя у которого хотите сбросить хвид")
            bot.register_next_step_handler (us_id, hwid_res, bot)

        except Exception as e:
            print(str(e))



    def subscription(self, bot: telebot.TeleBot ,message:types.Message):
        try:
           
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()
            id = message.chat.id

            cur.execute(f"SELECT has_subscription FROM records WHERE user_id = {id}")
            has_sub = cur.fetchone()

            if has_sub[0] == True:


                cur.execute(f"SELECT time_subscription FROM records WHERE user_id = {id}")
                date = cur.fetchone()
                splitted = date[0].split("-")
                end_date = datetime.date(int(splitted[0]), int(splitted[1]), int(splitted[2]))
            
                delta_date = end_date - datetime.date.today()

                bot.send_message(id, "Your subscription expiried at " + str(date[0]) + "\nDays left: " + str(delta_date.days))
            else:
                bot.send_message(id, "You haven't got any subscriptions yet")

            cur.close()
            connect.close()

        except Exception as e:
            print(str(e))

    def ban_start(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            us_id = bot.send_message(message.chat.id, "Введите id юзера для бана")     
            bot.register_next_step_handler (us_id, ban, bot)       
        except Exception as e:
            print(str(e))


    def unban_start(self, bot: telebot.TeleBot ,message:types.Message):
        try:
            us_id = bot.send_message(message.chat.id, "Введите id юзера для разбана")     
            bot.register_next_step_handler (us_id, unban, bot)     
        except Exception as e:
            print(str(e))

    def check_status(self, message:types.Message):
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()

            cur.execute(f"SELECT admin, reseller FROM records WHERE user_id = {message.chat.id}")
            prev = cur.fetchone()
            cur.close()
            connect.close()
            if prev[0] == True:
                return 2
            elif prev[1] == True:
                return 1
            else:
                return 0
            
        except Exception as e:
            print(str(e))



    def CheckAcc(self, str_, words):
        for word in words:
            if word in str_:
                return True
        return False






#------------------------------CLASS USING FUNCTIONS------------------------------
def unban(message:types.Message, bot: telebot.TeleBot):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()

        cur.execute(f" UPDATE records SET ban = False WHERE user_id = {message.text}")
        connect.commit()
        bot.send_message(message.chat.id, "Пользователь успешно разбанен")
        bot.send_message(message.text, "Вам восстановлен доступ к услугам!")
        cur.close()
        connect.close()
    except Exception as e:
        print(str(e))

def ressler_add(message:types.Message, bot: telebot.TeleBot):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()

        id = message.text

        cur.execute(f" UPDATE records SET reseller = True WHERE user_id = {id}")
        connect.commit()

        bot.send_message(message.chat.id, "Пользователю успешно выдана роль ресселлера")
        bot.send_message(message.text, "Вам выдана роль: Reseller")

        cur.close()
        connect.close()
    except Exception as e:
        print(str(e))


def ressler_del(message:types.Message, bot: telebot.TeleBot):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()

        id = message.text

        cur.execute(f" UPDATE records SET reseller = False WHERE user_id = {id}")
        connect.commit()

        bot.send_message(message.chat.id, "У пользователя успешно отобрана роль ресселлера")
        bot.send_message(message.text, "Вас лиишили роли: Reseller")

        cur.close()
        connect.close()
    except Exception as e:
        print(str(e))


def ban(message:types.Message, bot: telebot.TeleBot):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()
       
        cur.execute(f" UPDATE records SET ban = True WHERE user_id = {message.text}")
        connect.commit()
        bot.send_message(message.chat.id, "Пользователь успешно забанен")
        bot.send_message(message.text, "Вам ограничен доступ к услугам")
        cur.close()
        connect.close()
    except Exception as e:
        print(str(e))


def give_sub_count(message:types.Message, bot: telebot.TeleBot, id):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()


        cur.execute(f"SELECT admin, reseller FROM records WHERE user_id = {id}")
        prev = cur.fetchone()
        if prev[1] == 1 or prev[0] == 1:
            cur.execute(f"SELECT reseller_sub_count FROM records WHERE user_id = {id}")
            st_s_c = cur.fetchone()
            inf = [int(str(st_s_c[0])) + int(message.text), id]   
            cur.execute("UPDATE records SET reseller_sub_count = %s WHERE user_id = %s", inf)
            connect.commit()
            bot.send_message(message.chat.id, "Пользователю успешно добавлена возможность выдавать подписки\nПользователь осведомлен")
            bot.send_message(id, "Вам начисленно " + message.text + " подписок для выдачи\nВсего: " + str(inf[0]) )
            cur.close()
            connect.close()
            return
        else:
            bot.send_message(message.chat.id, "Похоже на то что он женщина, у него нет прав")
            cur.close()
            connect.close()
            return

    except Exception as e:
        print(str(e))

def hwid_res( message:types.Message, bot: telebot.TeleBot ):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()
        id = message.text

        cur.execute(f" UPDATE records SET hwid = NULL WHERE user_id = {id}")
        connect.commit()

        bot.send_message(message.chat.id, "Пользователю с id = " + message.text + " успешно сброшен HWID. Пользователь уведомлён")
        bot.send_message(id, "Ваш HWID был успешно сброшен")
        cur.close()
        connect.close()

    except Exception as e:
        print(str(e))


def SetPass(message:types.Message, bot: telebot.TeleBot):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()

        inf = [message.text, message.chat.id]   
        cur.execute("UPDATE records SET password = %s WHERE user_id = %s", inf)
        connect.commit()

        cur.execute(f"SELECT admin, reseller FROM records WHERE user_id = {message.chat.id}")
        prev = cur.fetchone()
        if prev[0] == True:
            bot.send_message(inf[1], "Пароль успешно добавлен", reply_markup= adm_kb)

        elif prev[1] == True:
            bot.send_message(inf[1], "Пароль успешно добавлен", reply_markup= res_kb)
        else:
            bot.send_message(inf[1], "Пароль успешно добавлен", reply_markup= user_kb)
        cur.close()
        connect.close()

    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "Пароль не добавлен")