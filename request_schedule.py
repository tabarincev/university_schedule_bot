import requests
import config 

from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.url = config.URL
        self.html = self.get_html(self.url)
        
    def get_html(self, url):
        response = requests.get(url, headers=config.HEADER) 
        return response.text

    def get_group_list(self, faculty_id):
        soup = BeautifulSoup(self.html, 'html.parser')
        table = soup.find('div', class_='vt251').find_all('div', class_='vt255')
        
        groups = {}
        ids = table[faculty_id].find_all('a')                          
        
        for row in ids:
            group_id = row.get('href').split('=')[1]
            group_name = row.get('data-nm')
            groups[group_name] = int(group_id)

        return groups
        
    def get_all_groups(html=get_html(config.URL)):
      soup = BeautifulSoup(html, 'html.parser')
      table = soup.find('div', class_='vt251').find_all('div', class_='vt255')

      group_list = []

      for index, el in enumerate(table):
          id = el.find_all('a')   # ссылки на все группы одного факультета

          for row in id:
              group_name = row.get('data-nm')
              group_list.append(group_name)

        return group_list
        
    def get_schedule(self, group_id, datetime_obj):
        day_index = datetime_obj.weekday() + 1              # int от 1 до 6
        
        if day_index == 7:
            return '_Занятий нет_'

        date = get_date_list(datetime_obj)                  # [2021, 09, 05]

        group_url = self.url + '?group={}&date={}-{}-{}'.format(group_id, *date)

        html = self.get_html(group_url)
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('div', class_='vt236')            # вся таблица              
        dates = table.find_all('div', class_='vt237')       # 05.09 понедельник

        lessons_class = 'vt239 rasp-day rasp-day{}'.format(day_index)
        lessons_by_day = table.find_all('div', class_=lessons_class)      

        N = len(lessons_by_day)                             # общее кол-во пар


        time_lessons = {1: '9:00 - 10:35', 2: '10:45 - 12:20',
                        3: '13:00 - 14:35', 4: '14:45 - 16:20',
                        5: '16:30 - 18:05', 6: '18:15 - 19:50'}


        input_schedule = ''

        
        for i in range(N):
            if lessons_by_day[i].text != '':
                # название предмета
                lesson_name = lessons_by_day[i].find('div', 
                                                     class_='vt240').text.strip()
                # ФИО преподавателя
                teacher_name = lessons_by_day[i].find('div', 
                                                      class_='vt241').text.strip()
                # аудитория 
                lesson_room = lessons_by_day[i].find('div', 
                                                     class_='vt242').text.strip()
                # тип занятия 
                lesson_type = lessons_by_day[i].find('div', 
                                                     class_='vt243').text.strip()
                # время занятия 
                lesson_time = time_lessons[i + 1]

                input_schedule += lesson_time + '\n'
                input_schedule += '{}.  *{}*'.format(i + 1, lesson_name) + '\n'
                input_schedule += '     _{}_'.format(lesson_type) + '\n'
                input_schedule += '     {}'.format(teacher_name) + '\n' 
                input_schedule += '     {}'.format(lesson_room) + '\n' * 2
        
        return input_schedule


import datetime


# datetime_obj
def get_current_date(): 
    return datetime.datetime.today().date()             
    

# datetime list
def get_date_list(datetime_obj):
    return [datetime_obj.year, datetime_obj.month, datetime_obj.day]
