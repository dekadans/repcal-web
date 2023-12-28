from . import Resource
from datetime import date
from repcal import RepublicanDate
from ..celebration import find_celebration


class Date(Resource):
    def __init__(self, d: date) -> None:
        self.date = d
        self.republican = RepublicanDate.from_gregorian(d)
        self.celebration = find_celebration(self.republican)

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
                    "number_in_year": self.republican.get_day_in_year()
                },
                "week": {
                    "number_in_month": self.republican.get_week(),
                    "number_in_year": self.republican.get_week_in_year()
                },
                "month": {
                    "name": self.republican.get_month_name() if not self.republican.is_sansculottides() else 'Jours complémentaires',
                    "number": self.republican.get_month()
                },
                "year": {
                    "arabic": self.republican.get_year_arabic(),
                    "roman": self.republican.get_year_roman()
                },
                "celebrating": {
                    "id": self.celebration.uri,
                    "name": self.celebration.name
                }
            }
        }
