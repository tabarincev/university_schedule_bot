import telebot 


class ReplyKeyboard:
    def __init__(self, bot):
        self.bot = bot

    def faculty_markup(self, message, faculties):
        faculty_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        for i in range(len(faculties)):
            faculty_markup.row(*faculties[i])
        
        self.bot.send_message(message.from_user.id, 'Выбери свой факультет.', reply_markup=faculty_markup)

    def group_markup(self, message, groups_by_faculty):
        group_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        for i in range(len(groups_by_faculty)):
            group_markup.row(*groups_by_faculty[i])
        group_markup.row('Назад ⬅️')

        self.bot.send_message(message.chat.id, 'Выбери группу.', reply_markup=group_markup)
