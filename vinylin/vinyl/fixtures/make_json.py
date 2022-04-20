import json
from vinyl.data import countries

sample = [
    {
        "model": "myapp.person",
        "pk": 1,
        "fields": {
            "first_name": "John",
            "last_name": "Lennon"
        }
    },
]


def create_fixtures_json(countries_tuple):
    all_countries = []
    for tu in countries_tuple:
        all_countries.append(tu[1])

    result = []
    for i, country in enumerate(all_countries):
        element = {
            'model': 'vinyl.country',
            'pk': i + 1,
            'fields': {
                'name': country
            }
        }
        result.append(element)

    with open('countries_fixture.json', 'w+', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=True, indent=2)


if __name__ == '__main__':
    create_fixtures_json(countries.COUNTRY_CHOICES)
