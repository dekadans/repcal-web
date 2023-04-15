from abc import abstractmethod, ABC
from datetime import datetime, date, time
from repcal import RepublicanDate, DecimalTime


class Resource(ABC):
    @abstractmethod
    def type(self) -> str:
        pass

    def params(self) -> dict:
        return {}

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class ApiIndex(Resource):
    def type(self) -> str: return 'apiindex'

    def to_dict(self) -> dict:
        return {
            'name': 'repcal.info',
            'description': 'An API for accessing datetime data in the styles used by the French First Republic.'
        }


class Moment(Resource):
    def __init__(self, dt: datetime) -> None:
        self.unix = round(dt.timestamp())
        self.offset = int(dt.utcoffset().total_seconds() // 60)
        self.iso = dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    def type(self) -> str: return 'moment'

    def params(self) -> dict:
        return {
            'timestamp': self.unix,
            'offset': self.offset
        }

    def to_dict(self) -> dict:
        return {
            "iso": self.iso
        }


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


class Time(Resource):
    def __init__(self, t: time) -> None:
        self.time = t
        self.decimal = DecimalTime.from_standard_time(t)

    def type(self) -> str: return 'time'

    def params(self) -> dict:
        return {
            'hour': self.time.hour,
            'minute': self.time.minute,
            'second': self.time.second
        }

    def decimal_format(self) -> str:
        if max(self.decimal.hour, self.decimal.minute, self.decimal.second) == 0:
            return '0'

        h = self.decimal.hour
        m = f'{self.decimal.minute:02}' if max(self.decimal.minute, self.decimal.second) > 0 else ''
        s = f'{self.decimal.second:02}' if self.decimal.second > 0 else ''
        return f'0,{h}{m}{s}'.rstrip('0')

    def to_dict(self) -> dict:
        return {
            "texts": {
                "default": str(self.decimal),
                "decimal": self.decimal_format()
            },
            "attributes": {
                "hour": self.decimal.hour,
                "minute": self.decimal.minute,
                "second": self.decimal.second
            }
        }
