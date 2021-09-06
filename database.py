import psycopg2

from config import db_params


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(user=db_params['user'], 
                                           password=db_params['password'],
                                           host=db_params['host'],
                                           port=db_params['port'],
                                           database=db_params['database'])
        self.cursor = self.connection.cursor()

    def registrate_user(self, user_id):
        try:
            self.cursor.execute('INSERT INTO users (id, state, faculty, group_id) VALUES (%s, %s, %s, %s)', (user_id, 'start', None, None))
            self.connection.commit()
        except Exception as e:
            # пользователь уже был зарегистрирован
            self.update_state(user_id, 'start')

    def update_state(self, user_id, new_state):
        try:
            self.cursor.execute('UPDATE users SET state = %s WHERE id = %s', 
                               (new_state, user_id))
            self.connection.commit()
        except Exception as e:
            # нет пользователя с таким id
            self.connection.rollback()

    def update_faculty(self, user_id, new_faculty):
        try:
            self.cursor.execute('UPDATE users SET faculty = %s WHERE id = %s', 
                               (new_faculty, user_id))
            self.connection.commit()
        except:
            # нет пользователя с таким id или state 
            self.connection.rollback()

    def update_group(self, user_id, new_group):
        try:
            self.cursor.execute('UPDATE users SET group_id = %s WHERE id = %s', 
                               (new_group, user_id))
            self.connection.commit()
        except:
            # нет пользователя с таким id
            self.connection.rollback()

    def select_faculty(self, user_id):
        self.cursor.execute('SELECT faculty FROM users WHERE id = %s', [user_id])
        return self.cursor.fetchone()[0].strip()

    def select_group(self, user_id):
        self.cursor.execute('SELECT group_id FROM users WHERE id = %s', [user_id])
        return self.cursor.fetchone()[0].strip()
        
    def select_user_state(self, user_id):
        self.cursor.execute('SELECT state FROM users WHERE id = %s', [user_id])
        return self.cursor.fetchone()[0].strip()
