import telebot
import os
from you_tube_parser import search_youtube_videos
from forbes_parser import parser_bot

token = os.environ.get('api_motivation')  # api токен установлен в переменные окружения пк
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ ")


@bot.message_handler(commands=['forbes'])
def start_message(message):
    bot.send_message(message.chat.id, parser_bot())


@bot.message_handler(commands=['youtube'])
def start_message(message):
    user_text = message.text.split()
    if len(user_text) == 1:
        bot.send_message(message.chat.id, "Вы не указали поисковой запрос.")
    else:
        search_query = " ".join(user_text[1:])
        video_links = search_youtube_videos(search_query)
        for video in video_links:
            bot.send_message(message.chat.id, f'{video["title"]}\n{video["url"]}')


bot.infinity_polling()
