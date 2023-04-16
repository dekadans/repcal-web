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
