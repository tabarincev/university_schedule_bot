import telebot 
import datetime

import config
import keyboard
import request_schedule
import message_handler
import old_parser
import database


TOKEN = config.TOKEN

bot = telebot.TeleBot(TOKEN)
reply_keyboard = keyboard.ReplyKeyboard(bot)
parser = old_parser.Parser()
db = database.Database()

faculties = ['РТС', 'ИКСС', 'ИСиТ', 'ФФП', 'ЦЭУБИ', 'СЦТ', 'ИНО', 'ИМ', 'СПБКТ']


@bot.message_handler(commands=['start'])
def start_handler(message):
    db.registrate_user(message.chat.id)

    sep_facs = return_sep_list(faculties, 2)
    reply_keyboard.faculty_markup(message, sep_facs)


@bot.message_handler(func=lambda message: 
                     message.text in faculties, content_types=['text'])
def faculty_handler(message):
    db.update_faculty(message.chat.id, message.text)

    groups = select_groups(message.text)
    reply_keyboard.group_markup(message, groups)


@bot.message_handler(func=lambda message: 
                     message.text == 'Назад ⬅️', content_types=['text'])
def back_handler(message):
    start_handler(message)
    

@bot.message_handler(func=lambda message: 
                     message.text == 'Сегодня 📅', content_types=['text'])
def today_handler(message):
    date = old_parser.get_current_date() 

    try:
        group = db.select_group(message.chat.id)        # ИКПИ-71
        faculty = db.select_faculty(message.chat.id)    # ИКСС
        group_id = select_group_id(faculty, group)      # 58741
        
        schedule = parser.get_schedule(group_id, date)
        
        bot.send_message(message.chat.id, schedule, parse_mode='Markdown')
    except Exception:
        start_handler(message)

    
@bot.message_handler(func=lambda message: 
                     message.text == 'Завтра ➡️', content_types=['text'])
def tomorrow_handler(message):
    date = old_parser.get_current_date() + datetime.timedelta(days=1) 

    try:
        group = db.select_group(message.chat.id)        # ИКПИ-71
        faculty = db.select_faculty(message.chat.id)    # ИКСС
        group_id = select_group_id(faculty, group)      # 58741
        
        schedule = parser.get_schedule(group_id, date)
        
        bot.send_message(message.chat.id, schedule, parse_mode='Markdown')
    except:
        start_handler(message)


message_handler.message_handler_groups(bot, reply_keyboard)


def separate_list(groups, n):
    for i in range(0, len(groups), n):
        yield groups[i : i + n]


def return_sep_list(groups, n):
    group = list(separate_list(groups, n))
    return group


def get_faculty_id(faculty):
    return faculties.index(faculty)


def select_groups(faculty):
    faculty_id = faculties.index(faculty)
    groups = list(request_schedule.get_groups_list(faculty_id).keys())
     
    return return_sep_list(groups, 3)


def select_group_id(faculty, group):
    faculty_id = get_faculty_id(faculty)
    ids = request_schedule.get_groups_list(faculty_id)

    return ids[group]


bot.polling()
