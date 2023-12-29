from repcal import RepublicanDate
import json
import pkgutil


class Subject:
    def __init__(self, name: str, entity_id: str, wiki_page: str):
        self.name = name
        self.uri = 'https://www.wikidata.org/entity/' + entity_id
        self.wiki_html = 'https://en.wikipedia.org/wiki/' + wiki_page
        self.wiki_json = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + wiki_page


def get_observation_data():
    file_data = pkgutil.get_data(__name__, 'data/days.json')
    return json.loads(file_data)


def get_month_data():
    file_data = pkgutil.get_data(__name__, 'data/months.json')
    return json.loads(file_data)


def find_observation(republican_date: RepublicanDate) -> Subject:
    data = get_observation_data()

    celebration = data[republican_date.month_index][republican_date.month_day_index]

    return Subject(
        celebration.get('label'),
        celebration.get('id'),
        celebration.get('wiki')
    )


def find_month(republican_date: RepublicanDate) -> Subject:
    data = get_month_data()

    celebration = data[republican_date.month_index]

    return Subject(
        celebration.get('label'),
        celebration.get('id'),
        celebration.get('wiki')
    )


def get_all_observations():
    data = get_observation_data()
    flattened = [
        day for month in data for day in month
    ]
    return flattened
