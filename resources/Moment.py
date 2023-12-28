from datetime import datetime
from . import Resource


class Moment(Resource):
    def __init__(self, dt: datetime) -> None:
        self.datetime = dt
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
