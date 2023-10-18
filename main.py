import telebot
from telebot import types
import os
from you_tube_parser import search_youtube_videos
from forbes_parser import parser_bot
from you_tube_parser import url_youtube

token = os.environ.get('api_motivation')  # api токен установлен в переменные окружения пк
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🤑 Цитата Forbes")
    btn2 = types.KeyboardButton("Поиск-Youtube")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🤑 Цитата Forbes":
        bot.send_message(message.chat.id, parser_bot())
    elif message.text == "Поиск-Youtube":
        bot.send_message(message.chat.id, "Введите поисковой запрос для YouTube")
        bot.register_next_step_handler(message, url_youtube, bot)


# def url_youtube(message):
#     user_text = message.text.split()
#     if len(user_text) == 1:
#         bot.send_message(message.chat.id, "Вы не указали поисковой запрос.")
#     else:
#         search_query = " ".join(user_text)
#
#         video_links = search_youtube_videos(search_query)
#         for video in video_links:
#             bot.send_message(message.chat.id, f'{video["title"]}\n{video["url"]}')

bot.infinity_polling()
