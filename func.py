import telebot
from telebot import types
import requests
import datetime
import mysql.connector
import json
import base64
from github import Github
from github import InputGitTreeElement
import os
from pyqiwip2p import QiwiP2P

#-----------SUPER ADMIN------------
adm= [
    '1030297121',# FRZ
    '630035056'#HOHOL
]
#----------------------------------

#--------------------------------KB ZONE---------------------------------
next = types.InlineKeyboardMarkup(row_width=2)
button1 = types.InlineKeyboardButton("Далее", callback_data='next')
button2 = types.InlineKeyboardButton("Стоп", callback_data='stop')
next.add(button1, button2)

user_kb = telebot.types.ReplyKeyboardMarkup(True)
user_kb.row('Buy', 'Change password', 'Subscription')

adm_kb = telebot.types.ReplyKeyboardMarkup(True)
adm_kb.row('Ban', 'Unban', 'Give sub', 'fix prob')
adm_kb.row('Give sub count',  'HWID del', 'Reseller add', 'Reseller del')

res_kb = telebot.types.ReplyKeyboardMarkup(True)
res_kb.row('Give sub', 'HWID del', 'Get sub count')

hack = types.InlineKeyboardMarkup(row_width=2)
apexbut = types.InlineKeyboardButton("Apex", callback_data='apex')
valorantbut = types.InlineKeyboardButton("Valorant", callback_data='valorant')
hack.add(apexbut, valorantbut)

#hack = telebot.types.ReplyKeyboardMarkup(True)
#hack.row("Apex", "Valorant")

time = types.InlineKeyboardMarkup(row_width=3)
day = types.InlineKeyboardButton("1 day", callback_data='day')
week = types.InlineKeyboardButton("7 days", callback_data='week')
month = types.InlineKeyboardButton("31 days", callback_data='month')
time.add(day, week, month)

pay_check = types.InlineKeyboardMarkup(row_width=1)
Done = types.InlineKeyboardButton("Done", callback_data='done')
pay_check.add(Done)
#------------------------------------------------------------------------

#---------------Info for database connection----------------
config = {
  'user': 'sql11483579',
  'password': 'gznQv95GYD',
  'host': 'sql11.freemysqlhosting.net',
  'database': 'sql11483579'
}
#-----------------------------------------------------------
class Oplata(object):
    def init_pay(self, bot: telebot.TeleBot ,message:types.Message):
        """THE HARDEST FUNC"""    
        try:
            bot.send_message(message.chat.id, "Выберите продукт:", reply_markup=hack)
            
        except Exception as e:
            print(str(e))
    

    def valorant_init(self, bot: telebot.TeleBot ,message:types.Message):
        """VALORANT PAY INITION"""
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()

            inf = ["valorant", message.chat.id]   
            cur.execute("UPDATE records SET hack_type = %s WHERE user_id = %s", inf)
            connect.commit()

            bot.send_message(message.chat.id, "Выберите продолжительность подписки:", reply_markup= time)

            cur.close()
            connect.close()
        except Exception as e:
            print(str(e))


    def apex_init(self, bot: telebot.TeleBot ,message:types.Message):
        """APEX PAY INITION"""
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()


            inf = ["apex", message.chat.id]   
            cur.execute("UPDATE records SET hack_type = %s WHERE user_id = %s", inf)
            connect.commit()    

            bot.send_message(message.chat.id, "Выберите продолжительность подписки:", reply_markup= time)

            cur.close()
            connect.close()
        except Exception as e:
            print(str(e))
    
    def time_step(self, bot: telebot.TeleBot ,message:types.Message, data):
        """BILL GENERATING"""
        try:
            p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjBqa3Roay0wMCIsInVzZXJfaWQiOiI3OTk1MTI0ODU3NCIsInNlY3JldCI6ImRjMjk3NzkwYTAyNDVjMzZmM2MyMTJiYmQwZTEwMWQ1Y2VjZDRmMTVhOTVlMWQxZjQxZDI0ZmU5YjNjNjRmYmUifX0=")
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()

            cur.execute(f"SELECT hack_type FROM records WHERE user_id = {message.chat.id}")
            hack_type = cur.fetchone()
            stro  = hack_type[0]

               
            #cur.execute("UPDATE records SET bill_id = %s WHERE user_id = %s", inf)
            #connect.commit()
            inf = [str(data), message.chat.id]   
            cur.execute("UPDATE records SET bill_add_w = %s WHERE user_id = %s", inf)
            connect.commit()
            
            cur.close()
            connect.close()

            match str(stro).removeprefix("b'").removesuffix("'"):
                case "valorant":
                            
                    match str(data):
                        case "day":
                            bill = p2p.bill(amount=1, lifetime=15)#800
                            set_bill_id(bill, message)

                            bot.send_message(message.chat.id, str(bill.pay_url), reply_markup=pay_check)
                            
                        case "week":
                            bill = p2p.bill(amount=2000, lifetime=15)
                            set_bill_id(bill, message)
                            bot.send_message(message.chat.id, str(bill.pay_url), reply_markup=pay_check)
                        case "month":
                            bill = p2p.bill(amount=6400, lifetime=15)
                            set_bill_id(bill, message)
                            bot.send_message(message.chat.id, str(bill.pay_url), reply_markup=pay_check)
                case "apex":
                    
                    match str(data):
                        case "day":
                            bill = p2p.bill(amount=400, lifetime=15)
                            set_bill_id(bill, message)
                            bot.send_message(message.chat.id, str(bill.pay_url), reply_markup=pay_check)
                        case "week":
                            bill = p2p.bill(amount=1200, lifetime=15)
                            set_bill_id(bill, message)
                            bot.send_message(message.chat.id, str(bill.pay_url), reply_markup=pay_check)
                        case "month":
                            bill = p2p.bill(amount=3200, lifetime=15)
                            set_bill_id(bill, message)
                            bot.send_message(message.chat.id, str(bill.pay_url), reply_markup=pay_check)
            cur.close()
            connect.close()
        except Exception as e:
            cur.close()
            connect.close()
            print(str(e))

    def Check_bill(self, bot: telebot.TeleBot ,message:types.Message, dateend):
        """BILL CHECKING"""
        p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjBqa3Roay0wMCIsInVzZXJfaWQiOiI3OTk1MTI0ODU3NCIsInNlY3JldCI6ImRjMjk3NzkwYTAyNDVjMzZmM2MyMTJiYmQwZTEwMWQ1Y2VjZDRmMTVhOTVlMWQxZjQxZDI0ZmU5YjNjNjRmYmUifX0=")
        
        
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()
        
        cur.execute(f"SELECT bill_id FROM records WHERE user_id = {message.chat.id}")
        bill_ide = cur.fetchone()
        print(str(bill_ide[0]))
        
        match str(p2p.check(bill_id=str(bill_ide[0]).removeprefix("b'").removesuffix("'")).status):
            case "WAITING":
                bot.send_message(message.chat.id, "Платеж не прошел\n"+str(p2p.check(bill_id=str(bill_ide[0]).removeprefix("b'").removesuffix("'")).pay_url),reply_markup=pay_check)
            case "PAID":
                
                
                bot.send_message(message.chat.id, "Платеж успешно совершен")
                self.give_payed_sub(bot, message, dateend)



        

    def give_payed_sub(self, bot: telebot.TeleBot ,message:types.Message, dateend):
        """GIVING SUB FOR DUMB PENDOS WITH A LOT OF SHITTY CHEKS"""
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()
            #2012-12-01(ГГ-ММ-ДД)
            cur.execute(f"SELECT time_subscription FROM records WHERE user_id = {message.chat.id}")
            date = cur.fetchone()
            
            if date[0] is None:
                end_date = datetime.date.today()
                
            else:
                splitted = str(date[0]).split("-")
                end = datetime.date(int(splitted[0]), int(splitted[1]), int(splitted[2]))
                if end < datetime.date.today():
                    end_date = datetime.date.today()
                else:
                    end_date = end



            match str(dateend).removeprefix("b'").removesuffix("'"):
                case "day":
                    dik = datetime.date(end_date.year, end_date.month, end_date.day+1)
                    inf = [dik, message.chat.id]
                    cur.execute("UPDATE records SET time_subscription = %s, has_subscription = True WHERE user_id = %s", inf)
                    connect.commit()
                    cur.close()
                    connect.close()
                    
                case "week":
                    dik = datetime.date(end_date.year, end_date.month, end_date.day+7)
                    inf = [dik, message.chat.id]
                    cur.execute("UPDATE records SET time_subscription = %s, has_subscription = True WHERE user_id = %s", inf)
                    connect.commit()
                    cur.close()
                    connect.close()
                    
                case "month":
                    dik = datetime.date(end_date.year, end_date.month, end_date.day+31)
                    inf = [dik, message.chat.id]
                    cur.execute("UPDATE records SET time_subscription = %s, has_subscription = True WHERE user_id = %s", inf)
                    connect.commit()
                    cur.close()
                    connect.close()

            cur.close()
            connect.close()
        except Exception as e:
            cur.close()
            connect.close()
            print(str(e))
                



class Work(object):
    def start(self, bot: telebot.TeleBot ,message:types.Message):
        """SHITTY START FUNC TO REG OR WELCOME USER"""
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
                ban BOOL,
                bill_id TEXT,
                bill_add_w TEXT
            )""")
            connect.commit()

            cur.execute(f"SELECT user_id FROM records WHERE user_id = {id}")
            data = cur.fetchone()


            if data is None:

               
                cur.execute(f"INSERT INTO records(user_id, admin, reseller,reseller_sub_count, has_subscription, ban) VALUES({int(message.chat.id)}, False, False, 0, False, False)")
                connect.commit()

                password = bot.send_message(message.chat.id, "Добро пожаловать, введите пароль, который будет исопльзоваться для дальнейшей авторизации")
                bot.register_next_step_handler (password, SetPass, bot)
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
                    cur.close()
                    connect.close()
                elif prev[0] == True:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= adm_kb)
                    cur.close()
                    connect.close()
                elif prev[1] == True:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= res_kb)
                    cur.close()
                    connect.close()
                else:
                    bot.send_message(id, "С возвращением " + str(message.chat.username) + "!", reply_markup= user_kb)
                    cur.close()
                    connect.close()
                
            cur.close()
            connect.close()
                    
        except Exception as e:
            cur.close()
            connect.close()
            print(str(e))

    def help_init(self, bot: telebot.TeleBot ,message:types.Message):
        """MAKING QUESTION"""
        try:
            text = bot.send_message(message.chat.id, "Введите текст проблемы:")
            bot.register_next_step_handler (text, self.help, bot)
        except Exception as e:
            print(str(e))
    
    def fixing_problems(self, bot: telebot.TeleBot ,message:types.Message):
        """ANSWERING FOR TICKET SYSTEM"""
        try:
                       
            with open('log.json') as json_file:#opening questions
                data = json.load(json_file)#reading file
                
                try:
                    p = data['rec'][0]#trying to get first question(reale queue XD)
                except:
                    bot.send_message(message.chat.id, "Вау! Все вопросы закончились, спасибо за помощь")#if first(0 index) write is emty that means we haven't got any questions
                    return

                id = p['id']#getting id of bustard to send him answer
                otv =  bot.send_message(message.chat.id, "Date:"+str(p['date'])+"\nName: " + str(p['name']) + "\nID: "+str(p['id']) + "\nProblem:\n"+str(p['text']))#inf about question(send to adm)
                del(data['rec'][0])#del first question
                with open('log.json', "w") as json_file:
                    json.dump(data, json_file, indent=2 , ensure_ascii=False)#rewrite new question file
                push()#push this file
                bot.register_next_step_handler(otv, send, bot, id)#sending answer for our bustard
                del(data)#del data for reduce shit with repeating answer
                          
        except Exception as e:
            print(str(e))

    def download(self):
        """DOWNLOADING FRESH TICKETS"""
        url = 'https://raw.githubusercontent.com/FRZBin/logs/main/log.json' 
        r = requests.get(url) 
        print(str(r.content))
        with open('log.json', 'wb') as f: 
            f.write(r.content )
        del(r)

    def change_pass(seld, bot: telebot.TeleBot ,message:types.Message):#AHHAHA GENIUS
        pas = bot.send_message(message.chat.id, "Введите новый пароль:")
        bot.register_next_step_handler(pas, SetPass, bot)
        

    def help(self, message:types.Message, bot: telebot.TeleBot):
        """TICKET SYSTEM ADDING"""
        try:
        
            try:
                data = json.load(open('log.json'))
            except:
                data = {}
                data['rec']=[]
            
            data['rec'].append({      
                'date': str(datetime.datetime.now()).split(".")[0],
                'id': message.chat.id,
                'name': message.chat.username,
                'text': message.text
            })
            
            with open('log.json', 'w') as outfile:
                json.dump(data, outfile, indent=2, ensure_ascii=False)

            push()
            bot.send_message(message.chat.id, "Ваш вопрос отправлен на рассмотрение. Ответ придёт в ближайшее время")
            
        except Exception as e:
            print(str(e))
        


    def give_sub_init(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR SUB GIVING"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя которому хотите выдать подписку")
            bot.register_next_step_handler (us_id, self.give_sub_date, bot)
        except Exception as e:
            print(str(e))

    def give_sub_date(self,message:types.Message, bot: telebot.TeleBot):
        """GETTING END DATE FOR SUB GIVING"""
        try:
            date = bot.send_message(message.chat.id, "Введите дату окончания подписки для пользователя\nПример: 2012-12-01(ГГ-ММ-ДД)")
            bot.register_next_step_handler (date, give_sub, bot, message.text)
        except Exception as e:
            print(str(e))

    def get_sub_count(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING SUB COUNT"""
        try:
            connect = mysql.connector.connect(**config)
            cur = connect.cursor()
            id = message.chat.id
            cur.execute(f"SELECT reseller_sub_count FROM records WHERE user_id = {id}")
            res = cur.fetchone()
            bot.send_message(id, "Всего возможностей выдать подписок: " + str(res[0]))
            cur.close()
            connect.close()
        except Exception as e:
            cur.close()
            connect.close()
            print(str(e))


    def resseler_add_init(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR RESSELER ADDING"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя которому хотите выдать роль реселера")
            bot.register_next_step_handler (us_id, ressler_add, bot)
        except Exception as e:
            print(str(e))


    def resseler_del_init(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR RESSELER REMOVING"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя у которого хотите отобрать роль реселера")
            bot.register_next_step_handler (us_id, ressler_del, bot)
        except Exception as e:
            print(str(e))

    def give_sub_count_start(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR SUB GIVING"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя которому хотите выдать возможность раздачи подписки")
            bot.register_next_step_handler (us_id, self.give_sub_count_int, bot)
        except Exception as e:
            print(str(e))

    def give_sub_count_int(self,message:types.Message, bot: telebot.TeleBot):
        """GETTING COUNT OF OPORTUNITIES FOR SUB GIVING"""
        try:         
            sub_count = bot.send_message(message.chat.id, "Введите количество подписок возможных для выдачи юзером с id = " + str(message.text))
            bot.register_next_step_handler (sub_count, give_sub_count, bot, message.text)

        except Exception as e:
            print(str(e))
        
    def hwid_res_start(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR HWID RESET"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id пользователя у которого хотите сбросить хвид")
            bot.register_next_step_handler (us_id, hwid_res, bot)

        except Exception as e:
            print(str(e))


#-----------------------------------------------------USELESS---------------------------------------------------------------
    def j(self, bot: telebot.TeleBot ,message:types.Message):
        """USELESS FUNC FOR TEST"""
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()
        dak = datetime.date(2022, 3, 12)
        
        inf = [dak, message.chat.id]
        cur.execute("UPDATE records SET time_subscription = %s, has_subscription = True WHERE user_id = %s", inf)
        connect.commit()
        cur.close()
        connect.close()

    def delete(self):
        try:
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log.json')
            os.remove(path)
        except Exception as e:
            print(str(e))
#---------------------------------------------------------------------------------------------------------------------------


    def subscription(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING AND SENDING ENDING OF SUB"""
       # try:
           
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()
        id = message.chat.id

        cur.execute(f"SELECT has_subscription FROM records WHERE user_id = {id}")
        has_sub = cur.fetchone()

        if has_sub[0] == True:


            cur.execute(f"SELECT time_subscription FROM records WHERE user_id = {id}")
            date = cur.fetchone()
            if date[0] is None:
                return
            cur.close()
            connect.close()
            print(date)
            splitted = str(date[0]).split("-")
            #print(splitted)
            end_date = datetime.date(int(splitted[0]), int(splitted[1]), int(splitted[2]))
            
        
            delta_date = end_date - datetime.date.today()
            if end_date < datetime.date.today():
                bot.send_message(id, "You haven't got any subscriptions yet")
                
                
            else:
                bot.send_message(id, "Your subscription expiried at " + str(date[0]) + "\nDays left: " + str(delta_date.days))
        else:
            cur.close()
            connect.close()
            bot.send_message(id, "You haven't got any subscriptions yet")

        cur.close()
        connect.close()

        #except Exception as e:
            #cur.close()
            #connect.close()
            #print(str(e))

    def ban_start(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR BAN"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id юзера для бана")     
            bot.register_next_step_handler (us_id, ban, bot)       
        except Exception as e:
            print(str(e))


    def unban_start(self, bot: telebot.TeleBot ,message:types.Message):
        """GETTING USER'S ID FOR UNBAN"""
        try:
            us_id = bot.send_message(message.chat.id, "Введите id юзера для разбана")     
            bot.register_next_step_handler (us_id, unban, bot)     
        except Exception as e:
            print(str(e))

    def check_status(self, message:types.Message):
        """ROLE CHECKING"""
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
            cur.close()
            connect.close()
            print(str(e))



    def CheckAcc(self, str_, words):
        """SUPER ADMIN CHECKING"""
        for word in words:
            if word in str_:
                return True
        return False






#------------------------------CLASS USING FUNCTIONS------------------------------
def unban(message:types.Message, bot: telebot.TeleBot):
    """USER UNABNING"""
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
        cur.close()
        connect.close()
        print(str(e))

def ressler_add(message:types.Message, bot: telebot.TeleBot):
    """RESSELER ADDING"""
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
        cur.close()
        connect.close()
        print(str(e))


def ressler_del(message:types.Message, bot: telebot.TeleBot):
    """REMOVE RESSELER ROLE"""
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
        cur.close()
        connect.close()
        print(str(e))


def ban(message:types.Message, bot: telebot.TeleBot):
    """USER BAN"""
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
        cur.close()
        connect.close()
        print(str(e))


def give_sub_count(message:types.Message, bot: telebot.TeleBot, id):
    """GIVING SUB COUNT"""
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
        cur.close()
        connect.close()
        print(str(e))

def hwid_res( message:types.Message, bot: telebot.TeleBot ):
    """HWID RESET"""
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
        cur.close()
        connect.close()
        print(str(e))


def give_sub(message:types.Message, bot: telebot.TeleBot, id):
    """GIVING SUB"""
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()
        inf = [message.text, id]
        cur.execute("UPDATE records SET time_subscription = %s, has_subscription = True WHERE user_id = %s", inf)
        connect.commit()

        cur.close()
        connect.close()
        bot.send_message(message.chat.id, "Пользователю успешно дана подписка\nОн осведомлён")
        bot.send_message(id, "Вам продлили подписку до " + str(message.text))
    except Exception as e:
        cur.close()
        connect.close()
        print(str(e))



def SetPass(message:types.Message, bot: telebot.TeleBot):
    """SETTING PASSWORD FOR NEW USER"""
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
        cur.close()
        connect.close()
        bot.send_message(message.chat.id, "Пароль не добавлен")


def push():
    """PUSHING TO GITHUB"""
    try:
        g = Github("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")
        repo = g.get_user().get_repo('lg') 

        file_list = [
            'log.json'
        ]
        file_names = [
            'log.json'
        ]
        commit_message = str(datetime.date.today())
        master_ref = repo.get_git_ref('heads/main')

        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)
        
        element_list = list()
        for i, entry in enumerate(file_list):
            with open(entry) as input_file:
                data = input_file.read()
            if entry.endswith('.png'): 
                data = base64.b64encode(data)
            element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
            element_list.append(element)

        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_message, tree, [parent])
        master_ref.edit(commit.sha)
    except Exception as e:
        print(str(e))

def send(message:types.Message, bot: telebot.TeleBot, id):
    """SENDING TICKET ANSWER TO USER"""
    try:
        bot.send_message(id, "Ответ на ваш недавний вопрос:\n"+ str(message.text))
        bot.send_message(message.chat.id, "Ответ успешно отправлен", reply_markup=next)
    except Exception as e:
        print(str(e))

   

def set_bill_id(bill, message:types.Message):
    try:
        connect = mysql.connector.connect(**config)
        cur = connect.cursor()

        inf = [str(bill.bill_id), message.chat.id]   
        cur.execute("UPDATE records SET bill_id = %s WHERE user_id = %s", inf)
        connect.commit()
        cur.close()
        connect.close()
    except Exception as e:
        cur.close()
        connect.close()
        print(str(e))

