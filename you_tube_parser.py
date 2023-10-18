import os
from googleapiclient.discovery import build
import telebot

token = os.environ.get('api_motivation')  # api токен установлен в переменные окружения пк
bot = telebot.TeleBot(token)

api_key = os.environ.get('api_you')  # апи ключ ютуба установлен в переменные окружения пк


def search_youtube_videos(query, api_key=api_key, max_results=5):
    youtube = build('youtube', 'v3', developerKey=api_key)

    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video = {
            'title': search_result['snippet']['title'],
            'video_id': search_result['id']['videoId'],
            'url': f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
        }
        videos.append(video)

    return videos


def url_youtube(message, bot=None):
    user_text = message.text.split()
    if len(user_text) == 1:
        bot.send_message(message.chat.id, "Вы не указали поисковой запрос.")
    else:
        search_query = " ".join(user_text)

        video_links = search_youtube_videos(search_query)
        for video in video_links:
            bot.send_message(message.chat.id, f'{video["title"]}\n{video["url"]}')
# if __name__ == "__main__":
#     # api_key = os.environ.get('api_you')
#     query = "как научится программировать"
#     results = search_youtube_videos(query, api_key)
#
#     for index, video in enumerate(results, start=1):
#         print(f'{index}. {video["title"]}')
#         print(f'   URL: {video["url"]}')
