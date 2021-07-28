import telebot 
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start_handler(m):
    pass


bot.polling(none_stop=True)
