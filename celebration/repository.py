from repcal import RepublicanDate
import json
import pkgutil


class Subject:
    def __init__(self, name: str, wiki_id: str):
        self.name = name
        self.wiki_id = wiki_id


def get_data():
    file_data = pkgutil.get_data(__name__, 'data.json')
    return json.loads(file_data)


def find(republican_date: RepublicanDate) -> Subject:
    data = get_data()

    celebration = data[republican_date.month_index][republican_date.month_day_index]

    return Subject(celebration.get('label'), celebration.get('wiki'))


def get_all():
    data = get_data()
    flattened = [
        day for month in data for day in month
    ]
    return flattened
