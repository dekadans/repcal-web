from . import Resource
from datetime import date
from repcal import RepublicanDate


class Date(Resource):
    def __init__(self, d: date) -> None:
        self.date = d
        self.republican = RepublicanDate.from_gregorian(d)
        rep_date_str = str(self.republican)
        self.formatted = rep_date_str[0].upper() + rep_date_str[1:]

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
                "default": self.formatted
            },
            "attributes": {
                "complementary": self.republican.is_sansculottides(),
                "day": {
                    "name": self.republican.get_weekday(),
                    "number_in_week": self.republican.week_day_index+1,
                    "number_in_month": self.republican.get_day()
                },
                "week": {
                    "number_in_month": self.republican.get_week_number(),
                    "number_in_year": (self.republican.get_week_number() + self.republican.month_index * 3)
                } if not self.republican.is_sansculottides() else None,
                "month": {
                    "name": self.republican.get_month(),
                    "number": self.republican.month_index+1
                } if not self.republican.is_sansculottides() else None,
                "year": {
                    "arabic": self.republican.get_year_arabic(),
                    "roman": self.republican.get_year_roman()
                }
            }
        }
