import json

import country_choices


def create_countries_fixture(countries_tuple):
    all_countries = [tu[1] for tu in countries_tuple]

    result = [
        {
            'model': 'vinyl.country',
            'pk': i + 1,
            'fields': {'name': country}
        } for i, country in enumerate(all_countries)
    ]

    with open('../fixtures/countries.json', 'w+', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=True, indent=2)


if __name__ == '__main__':
    create_countries_fixture(country_choices.COUNTRY_CHOICES)
