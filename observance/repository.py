import json
import pkgutil


class Subject:
    def __init__(self, name: str, entity_id: str, wiki_page: str):
        self.name = name
        self.id = entity_id
        self.wiki_html = 'https://en.wikipedia.org/wiki/' + wiki_page


def get_observation_data():
    file_data = pkgutil.get_data(__name__, 'data/days.json')
    return json.loads(file_data)


def get_month_data():
    file_data = pkgutil.get_data(__name__, 'data/months.json')
    return json.loads(file_data)


def get_day_by_index(index: int) -> Subject:
    m = index // 30
    d = index % 30
    data = get_observation_data()
    observance = data[m][d]
    return Subject(
        observance.get('label'),
        observance.get('id'),
        observance.get('wiki')
    )


def get_month_by_index(index: int) -> Subject:
    m = index // 30
    data = get_month_data()
    observance = data[m]
    return Subject(
        observance.get('label'),
        observance.get('id'),
        observance.get('wiki')
    )


def get_all_observations():
    data = get_observation_data()
    flattened = [
        day for month in data for day in month
    ]
    return flattened
