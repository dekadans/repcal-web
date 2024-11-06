from .HALResponse import HALResponse
from ..resources import Date, Observance
from .links import Curie, Link


class DateResponse(HALResponse):
    def __init__(self, d: Date, e) -> None:
        super().__init__(d, e)

        self.add_curie(Curie('repcal'))

        observance_rel = 'repcal:observance'
        if observance_rel in self.requested_embeds:
            self.add_embedded(observance_rel, Observance(d.republican.get_day_in_year()))
        else:
            self.add_link(Link(
                rel=observance_rel,
                endpoint='observance_resource',
                params={
                    'index': d.republican.get_day_in_year()
                }
            ))
