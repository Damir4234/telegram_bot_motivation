import os
from googleapiclient.discovery import build

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


# if __name__ == "__main__":
#     # api_key = os.environ.get('api_you')
#     query = "как научится программировать"
#     results = search_youtube_videos(query, api_key)
#
#     for index, video in enumerate(results, start=1):
#         print(f'{index}. {video["title"]}')
#         print(f'   URL: {video["url"]}')
