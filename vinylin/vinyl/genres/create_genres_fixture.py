import json

from bs4 import BeautifulSoup
import requests


GENRES_SITE = 'https://www.chosic.com/list-of-music-genres/'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) '
                   'Gecko/20100101 Firefox/71.0'),
    'accept': '*/*'
}


def get_raw_html(url, params=None):
    return requests.get(url, params=params, headers=HEADERS).text


def get_genres() -> list:
    html = get_raw_html(GENRES_SITE)
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all('li', 'capital-letter genre-term')

    genres = [li.string.title() for li in lis]
    genres.sort()
    return genres


def make_fixture():
    genres = get_genres()
    result = [
        {
            'model': 'vinyl.genre',
            'pk': i + 1,
            'fields': {'title': genre}
        } for i, genre in enumerate(genres)
    ]

    with open('../fixtures/genres.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=True, indent=2)


if __name__ == '__main__':
    make_fixture()
