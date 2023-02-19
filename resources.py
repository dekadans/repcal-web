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
    def type(self) -> str: return 'api'

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
            "text": self.formatted,
            "attributes": {
                "sansculottides": self.republican.is_sansculottides(),
                "day": self.republican.get_day(),
                "week": self.republican.get_week_number(),
                "weekday": self.republican.get_weekday(),
                "month": self.republican.get_month(),
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

    def to_dict(self) -> dict:
        return {
            "text": str(self.decimal),
            "attributes": {
                "hour": self.decimal.hour,
                "minute": self.decimal.minute,
                "second": self.decimal.second
            }
        }
