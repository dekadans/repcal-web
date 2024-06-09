from . import Resource
from datetime import date
from repcal import RepublicanDate
from ..metadata import find_observation, find_month


class Date(Resource):
    def __init__(self, d: date) -> None:
        self.date = d
        self.republican = RepublicanDate.from_gregorian(d)
        self.day_entity = find_observation(self.republican)
        self.month_entity = find_month(self.republican)

    def type(self) -> str: return 'date'

    def params(self) -> dict:
        return {
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day
        }

    def to_dict(self) -> dict:
        return {
            "texts": {
                "default": str(self.republican)
            },
            "attributes": {
                "complementary": self.republican.is_sansculottides(),
                "day": {
                    "name": self.republican.get_day_name(),
                    "number_in_week": self.republican.get_day_in_week(),
                    "number_in_month": self.republican.get_day(),
                    "number_in_year": self.republican.get_day_in_year(),
                    "entity": {
                        "id": self.day_entity.id,
                        "name": self.day_entity.name
                    }
                },
                "week": {
                    "number_in_month": self.republican.get_week(),
                    "number_in_year": self.republican.get_week_in_year()
                },
                "month": {
                    "name": self.republican.get_month_name() if not self.republican.is_sansculottides() else 'Jours complémentaires',
                    "number": self.republican.get_month(),
                    "entity": {
                        "id": self.month_entity.id,
                        "name": self.month_entity.name
                    }
                },
                "year": {
                    "arabic": self.republican.get_year_arabic(),
                    "roman": self.republican.get_year_roman()
                }
            }
        }
