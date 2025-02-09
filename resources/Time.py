from . import Resource
from datetime import time
from repcal import DecimalTime


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
            "texts": {
                "default": str(self.decimal),
                "decimal": self.decimal.decimal
            },
            "attributes": {
                "hour": self.decimal.hour,
                "minute": self.decimal.minute,
                "second": self.decimal.second
            }
        }
