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


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🤑  Цитата Forbes")
    btn2 = types.KeyboardButton("🎥  Поиск-Youtube")
    btn3 = types.KeyboardButton("Заметка")
    btn4 = types.KeyboardButton("Мои заметки")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🤑  Цитата Forbes":
        bot.send_message(message.chat.id, parser_bot())
    elif message.text == "🎥  Поиск-Youtube":
        bot.send_message(message.chat.id, "Введите поисковой запрос для YouTube")
        bot.register_next_step_handler(message, url_youtube, bot)
    elif message.text == "Заметка":
        bot.send_message(message.chat.id, "Введите текст заметки")
        bot.register_next_step_handler(message, add_note)
    elif message.text == "Мои заметки":
        view_notes(message)


@bot.message_handler(func=lambda message: True)
def add_note(message):
    user_id = message.from_user.id
    user_note = message.text
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    insert_query = "INSERT INTO notes (user_id, note_text) VALUES (%s, %s)"
    cursor.execute(insert_query, (user_id, user_note))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Заметка добавлена в базу данных!")


@bot.message_handler(commands=['view_notes'])
def view_notes(message):
    user_id = message.from_user.id
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("SELECT note_text FROM notes WHERE user_id = %s", (user_id,))
    notes = cursor.fetchall()
    conn.close()

    if notes:

        notes_text = "\n".join([note[0] for note in notes])
        bot.send_message(message.chat.id, "Ваши заметки:\n" + notes_text)
    else:
        bot.send_message(message.chat.id, "У вас пока нет заметок.")


bot.infinity_polling()
