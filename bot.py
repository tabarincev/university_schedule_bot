import telebot
import config
import keyboard

from request_schedule import get_all_groups, get_faculties_list
from request_schedule import get_groups_list, separate_list


bot = telebot.TeleBot(config.TOKEN)
reply_keyboard_markup = keyboard.ReplyKeyboard(bot)

faculties_list = get_faculties_list()
groups_list = get_all_groups()


@bot.message_handler(commands=['start'])
def start_handler(message):
    faculties = list(separate_list(faculties_list, 2))
    reply_keyboard_markup.faculty_markup(message, faculties)


@bot.message_handler(func=lambda message: 
                     message.text in faculties_list, content_types=['text'])
def faculty_handler(message):
    faculty_id = faculties_list.index(message.text)

    groups = list(get_groups_list(faculty_id).keys())
    groups = list(separate_list(groups, 3))

    reply_keyboard_markup.group_markup(message, groups)


@bot.message_handler(func=lambda message: 
                     message.text in groups_list, content_types=['text'])
def group_handler(message):
    reply_keyboard_markup.display_schedule_markup(message)


@bot.message_handler(func=lambda message: 
                     message.text == 'Сегодня 📅', content_types=['text'])
def today_schedule_handler(message):
    pass


@bot.message_handler(func=lambda message: 
                     message.text == 'Завтра ➡️', content_types=['text'])
def tomorrow_schedule_handler(message):
    pass


@bot.message_handler(func=lambda message: 
                     message.text == 'Назад ⬅️', content_types=['text'])
def back_button_handler(message):
    pass



bot.polling(none_stop=True)
