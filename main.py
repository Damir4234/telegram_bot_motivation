import telebot
from telebot import types
import os
from forbes_parser import parser_bot
from you_tube_parser import url_youtube
import psycopg2

db_params = {
    'dbname': 'your_database_name',
    'user': 'your_database_user',
    'password': 'your_database_password',
    'host': 'your_database_host',
    'port': 'your_database_port'
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
    markup.add(btn1, btn2, btn3)
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


@bot.message_handler(func=lambda message: True)
def add_note(message):
    user_id = message.from_user.id
    user_note = message.text  # Используйте message.text напрямую
    with open(f'notes_{user_id}.txt', 'a') as file:
        file.write(user_note + '\t\n')
    bot.send_message(message.chat.id, "Заметка добавлена!")


bot.infinity_polling()
