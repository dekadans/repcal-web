from .HALResponse import HALResponse
from datetime import datetime
from ..resources import Moment, Date, Time
from .links import Curie


class MomentResponse(HALResponse):
    def __init__(self, dt: datetime) -> None:
        super().__init__(Moment(dt))

        self.add_curie(Curie('repcal'))
        self.add_embedded('repcal:date', Date(dt.date()))
        self.add_embedded('repcal:time', Time(dt.time()))
