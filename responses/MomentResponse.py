from .HALResponse import HALResponse
from .links import Curie
from ..resources import Moment, Date, Time


class MomentResponse(HALResponse):
    def __init__(self, moment: Moment, e) -> None:
        super().__init__(moment, e)

        self.add_link(Curie('repcal'))
        self.add_embedded('repcal:date', Date(moment.datetime.date()))
        self.add_embedded('repcal:time', Time(moment.datetime.time()))
