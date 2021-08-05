class Parser:
    def __init__(self):
        self.URL = 'https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya'
        self.header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Referer': 'https://www.sut.ru/'
    }   
        
    def get_html(self, url):
        response = requests.get(url, headers=header) 
        return response.text

    def get_faculties_list(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        table = soup.find('div', class_='vt251')

        return [faculty.text.strip() for faculty in table.find_all('div', class_='vt253')]

    def get_group_list(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        table = soup.find('div', class_='vt251').find_all('div', class_='vt255')
        dict_table = {}
        facs = ['РТС', 'ИКСС', 'ИСиТ', 'ФФП', 'ЦЭУБИ', 'СЦТ', 'ИНО', 'ИМ', 'Аспирантура', 'СПБКТ']

        for index, el in enumerate(table):
            id = el.find_all('a')                          # ссылки на все группы одного факультета
        
            tmp = {}

            for row in id:
                group_id = row.get('href').split('=')[1]
                group_name = row.get('data-nm')
            
                dict_table[group_name] = int(group_id)
        
        return dict_table

    def get_schedule(self, group_id, year, month, day):
        group_url = URL + '?group={}&date={}-{}-{}'.format(group_id, year, month, day)

        html = self.get_html(group_url)
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('div', class_='vt236')                # вся таблица
        dates = table.find_all('div', class_='vt237')           # строка дат и дней недели

        day_of_week = None   # день недели 
        index_of_day = None  # индекс дня недели

        indexes_day_week = {'понедельник': 1, 'вторник': 2,
                        'среда': 3, 'четверг': 4, 
                        'пятница': 5, 'суббота': 6}

        time_lessons = {1: '9:00 - 10:35', 2: '10:45 - 12:20',
                    3: '13:00 - 14:35', 4: '14:45 - 16:20',
                    5: '16:30 - 18:05'}

        index_to_month = {'01': 'января', '02': 'февраля',
                      '03': 'марта', '04': 'апреля', 
                      '05': 'мая', '06': 'июня',
                      '07': 'июля', '08': 'августа',
                      '09': 'сентября', '10': 'октября',
                      '11': 'ноября', '12': 'декабря'}

        for days in dates:
            if days.text.split()[0].strip() == '{}.{}'.format(day, month):
                day_of_week = days.text.split()[1].strip()
                index_of_day = indexes_day_week[day_of_week]

        lessons_class = 'vt239 rasp-day rasp-day{}'.format(index_of_day)   
        lessons_by_day = table.find_all('div', class_=lessons_class)      # столбец с парами

        N = len(lessons_by_day)
    
        input_schedule = '{}, {} {} {}'.format(day_of_week.capitalize(), day, index_to_month[month], year) + '\n' * 3
    
        for i in range(N):
            if lessons_by_day[i].text != '':
                # название предмета
                lesson_name = lessons_by_day[i].find('div', class_='vt240').text.strip()
    
                # преподаватель
                teacher_name = lessons_by_day[i].find('span', class_='teacher').text.strip()

                # аудитория 
                lesson_room = lessons_by_day[i].find('div', class_='vt242').text.strip()

                # тип занятия 
                lesson_type = lessons_by_day[i].find('div', class_='vt243').text.strip()

                # время занятия 
                lesson_time = time_lessons[i + 1]
            
                input_schedule += lesson_time + '\n'
                input_schedule += '{}. *{}*'.format(i + 1, lesson_name) + '\n'
                input_schedule += '    _{}_'.format(lesson_type) + '\n'
                input_schedule += '    {}'.format(teacher_name) + '\n' * 2

        return input_schedule
