from .HALResponse import HALResponse
from .links import Curie
from ..resources import Moment, Date, Time


class MomentResponse(HALResponse):
    def __init__(self, moment: Moment) -> None:
        super().__init__(moment)

        self.add_curie(Curie('repcal'))
        self.add_embedded('repcal:date', Date(moment.datetime.date()))
        self.add_embedded('repcal:time', Time(moment.datetime.time()))
