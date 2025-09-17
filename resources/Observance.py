from . import Resource
from ..observance import get_day_by_index, get_month_by_index
import re


class Observance(Resource):
    def __init__(self, day_number):
        index = day_number-1
        self.day = get_day_by_index(index)
        self.month = get_month_by_index(index)
        self.day_number = day_number

    def type(self) -> str: return 'observance'

    def params(self) -> dict:
        return {
            'index': self.day_number
        }

    def _get_texts(self) -> dict:
        if self.day_number > 360:
            day = self.day.name.lower()
            text = f"<observance><month>Complementary day</month> celebrating <day>{day}</day>.</observance>"
        else:
            month = self.month.name.lower()
            day = self.day.name.lower()
            text = f"<observance>The day of <day>{day}</day>, in the month of <month>{month}</month>.</observance>"

        return {
            "default": self._strip_tags(text),
            "tagged": text
        }

    def _strip_tags(self, text: str) -> str:
        return re.compile(r'(<!--.*?-->|<[^>]*>)').sub('', text)

    def to_dict(self) -> dict:
        return {
            'texts': self._get_texts(),
            'attributes': {
                'day': {
                    'id': self.day.id,
                    'name': self.day.name
                },
                'month': {
                    'id': self.month.id,
                    'name': self.month.name
                },
            }
        }

