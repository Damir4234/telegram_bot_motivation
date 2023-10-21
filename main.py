import telebot
from telebot import types
import os
from forbes_parser import parser_bot
from you_tube_parser import url_youtube
import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '050822',
    'host': 'localhost',
    'port': '5432'
}

token = os.environ.get('api_motivation')  # api токен установлен в переменные окружения пк
bot = telebot.TeleBot(token)


def table_exists(cursor, table_name):
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);", (table_name,))
    return cursor.fetchone()[0]


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    user_table_name = f'user_{user_id}'

    # Check if the user-specific table exists
    if not table_exists(cursor, user_table_name):
        # If the table doesn't exist, create it
        cursor.execute(f"CREATE TABLE {user_table_name} (note_id serial PRIMARY KEY, note_text text);")
        conn.commit()

    bot.send_message(message.chat.id, "Привет ✌️ ")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🤑  Цитата Forbes")
    btn2 = types.KeyboardButton("🎥  Поиск-Youtube")
    btn3 = types.KeyboardButton("📝  Запомнить заметку")
    btn4 = types.KeyboardButton("📝  Мои заметки")
    btn5 = types.KeyboardButton("❌  Удалить заметку")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🤑  Цитата Forbes":
        bot.send_message(message.chat.id, parser_bot())
    elif message.text == "🎥  Поиск-Youtube":
        bot.send_message(message.chat.id, "Введите поисковой запрос для YouTube")
        bot.register_next_step_handler(message, url_youtube, bot)
    elif message.text == "📝  Запомнить заметку":
        bot.send_message(message.chat.id, "Введите текст заметки")
        bot.register_next_step_handler(message, add_note)
    elif message.text == "📝  Мои заметки":
        view_notes(message)
    elif message.text == "❌  Удалить заметку":
        delete_note_prompt(message)
    else:
        bot.send_message(message.chat.id, "Выберите команду из меню, используя кнопки ниже👇👇👇")


@bot.message_handler(func=lambda message: True)
def add_note(message):
    user_id = message.from_user.id
    user_note = message.text
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    user_table_name = f'user_{user_id}'

    cursor.execute(f"SELECT MAX(note_id) FROM {user_table_name}")
    max_note_id = cursor.fetchone()[0]

    if max_note_id is None:
        max_note_id = 0

    next_note_id = max_note_id + 1
    insert_query = f"INSERT INTO {user_table_name} (note_id, note_text) VALUES (%s, %s)"
    cursor.execute(insert_query, (next_note_id, user_note))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Заметка добавлена в базу данных!")


@bot.message_handler(commands=['view_notes'])
def view_notes(message):
    user_id = message.from_user.id
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    user_table_name = f'user_{user_id}'

    cursor.execute(f"SELECT note_id, note_text FROM {user_table_name}")
    notes = cursor.fetchall()
    conn.close()

    if notes:
        notes_text = "\n".join([f"{note[0]}. {note[1]}" for note in notes])
        bot.send_message(message.chat.id, "Ваши заметки:\n" + notes_text)
    else:
        bot.send_message(message.chat.id, "У вас пока нет заметок.")


@bot.message_handler(commands=['delete_note'])
def delete_note_prompt(message):
    bot.send_message(message.chat.id, "Введите номер заметки, которую хотите удалить:")
    bot.register_next_step_handler(message, delete_note)


def delete_note(message):
    try:
        note_id_to_delete = int(message.text)
        user_id = message.from_user.id
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        user_table_name = f'user_{user_id}'

        cursor.execute(f"SELECT note_id FROM {user_table_name} WHERE note_id = %s", (note_id_to_delete,))
        existing_note = cursor.fetchone()

        if existing_note:

            cursor.execute(f"DELETE FROM {user_table_name} WHERE note_id = %s", (note_id_to_delete,))
            conn.commit()

            cursor.execute(f"UPDATE {user_table_name} SET note_id = note_id - 1 WHERE note_id > %s",
                           (note_id_to_delete,))
            conn.commit()

            conn.close()
            bot.send_message(message.chat.id, "Заметка была удалена!")
        else:
            bot.send_message(message.chat.id, "Заметка с указанным номером не найдена.")
    except ValueError:
        bot.send_message(message.chat.id, "Номер заметки должен быть числом.")


bot.infinity_polling()
