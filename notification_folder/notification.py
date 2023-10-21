import re
import psycopg2
import os
from notifiers import get_notifier
import time

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '050822',
    'host': 'localhost',
    'port': '5432'
}


def extract_user_id(table_name):
    print(1)
    # Извлекаем цифры из названия таблицы
    match = re.search(r'\d+', table_name)
    if match:
        return int(match.group())
    return None


def send_notifications_to_users():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    table_names = cursor.fetchall()

    user_ids = []  # Создаем пустой список для хранения user_id

    for table_name in table_names:
        user_id = extract_user_id(table_name[0])
        if user_id is not None:
            user_ids.append(user_id)  # Добавляем user_id в список

    conn.close()

    return user_ids


while True:
    user_ids = send_notifications_to_users()  # Получаем список user_id
    telegram = get_notifier("telegram")
    message_text = 'Проверьте ваши заметки!'
    time.sleep(3600.0)

    for user_id in user_ids:
        chat_id = str(user_id)  # Преобразуем user_id в строку для использования в chat_id
        telegram.notify(token=os.environ.get('api_motivation'), chat_id=chat_id, message=message_text)
        print(chat_id)
