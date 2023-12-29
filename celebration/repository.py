from repcal import RepublicanDate
import json
import pkgutil


class Subject:
    def __init__(self, name: str, entity_id: str, wiki_page: str):
        self.name = name
        self.uri = 'https://www.wikidata.org/entity/' + entity_id
        self.wiki_html = 'https://en.wikipedia.org/wiki/' + wiki_page
        self.wiki_json = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + wiki_page


def get_data():
    file_data = pkgutil.get_data(__name__, 'data.json')
    return json.loads(file_data)


def find(republican_date: RepublicanDate) -> Subject:
    data = get_data()

    celebration = data[republican_date.month_index][republican_date.month_day_index]

    return Subject(
        celebration.get('label'),
        celebration.get('id'),
        celebration.get('wiki')
    )


def get_all():
    data = get_data()
    flattened = [
        day for month in data for day in month
    ]
    return flattened
