from repcal import RepublicanDate
import json
import pkgutil


class Subject:
    def __init__(self, name: str, wiki_id: str):
        self.name = name
        self.wiki_id = wiki_id


def find(republican_date: RepublicanDate) -> Subject:
    file_data = pkgutil.get_data(__name__, 'data.json')
    data = json.loads(file_data)

    celebration = data[republican_date.month_index][republican_date.month_day_index]

    return Subject(celebration.get('label'), celebration.get('wiki'))
