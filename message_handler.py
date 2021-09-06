import request_schedule

from database import Database


db = Database()
group_list = request_schedule.Parser().get_all_groups()

def message_handler_groups(bot, keyboard):
    @bot.message_handler(func=lambda message: 
                         message.text in group_list, content_types=['text'])
    def get_selected_group(message):
        db.update_group(message.chat.id, message.text)
        return keyboard.display_schedule_markup(message)
