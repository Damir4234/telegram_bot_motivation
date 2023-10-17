import requests
from bs4 import BeautifulSoup
import random


# Кокрентная ссылка для этой функции
# 'https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat'

def parser_bot(url_str='https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat'):
    """
    Парсит цитаты и рандомно выбирает одну из ста

    Args:
            сслыку на страницу Forbes
    return:
            рандомная цитата
    """
    response = requests.get(url_str)
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_elements = soup.select('.CFaZ3 span')

    quotes = [quote.get_text() for quote in quote_elements]
    quotes_1 = quotes[::2]
    random_string = random.choice(quotes_1)
    index_quotes = quotes.index(random_string)
    quotes_2 = f"{random_string}\n\n{quotes[index_quotes + 1]}"
    return quotes_2


# print(parser_bot())
