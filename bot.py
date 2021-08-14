import telebot
import config
import keyboard

from timetable import Parser

parser = Parser()
bot = telebot.TeleBot(config.TOKEN)
reply_keyboard_markup = keyboard.ReplyKeyboard(bot)

faculties_list = parser.get_faculties_list()


@bot.message_handler(commands=['start'])
def start_handler(message):
    faculties = list(Parser.separate_list(faculties_list, 2))
    reply_keyboard_markup.faculty_markup(message, faculties)


@bot.message_handler(func=lambda message: 
                     message.text in faculties_list, content_types=['text'])
def faculty_handler(message):
    faculty_id = faculties_list.index(message.text)

    groups = list(parser.get_group_list(faculty_id).keys())
    groups = list(Parser.separate_list(groups, 3))

    reply_keyboard_markup.group_markup(message, groups)


@bot.message_handler(func=lambda message: message.text == 'Назад ⬅️', 
                     content_types=['text'])
def back_handler(message):
    pass


bot.polling(none_stop=True)
