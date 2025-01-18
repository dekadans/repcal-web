from . import Resource
from datetime import date
from repcal import RepublicanDate


class Date(Resource):
    def __init__(self, d: date) -> None:
        self.date = d
        self.republican = RepublicanDate.from_gregorian(d)

    def type(self) -> str: return 'date'

    def params(self) -> dict:
        return {
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day
        }

    def _get_short(self):
        f = '{%d} compl. / {%y}' if self.republican.is_sansculottides() else '{%d} / {%m} / {%y}'
        return self.republican.get_formatter().format(f)

    def to_dict(self) -> dict:
        return {
            "texts": {
                "default": str(self.republican),
                "short": self._get_short()
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
                    "roman": self.republican.get_year_roman(),
                    "leap": RepublicanDate.is_leap_year(self.republican.get_year_arabic())
                }
            }
        }
