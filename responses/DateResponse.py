from .HALResponse import HALResponse
from ..resources import Date
from .links import Curie, Link


class DateResponse(HALResponse):
    def __init__(self, d: Date) -> None:
        super().__init__(d)

        self.add_curie(Curie('repcal'))
        self.add_link(Link(
            rel='repcal:celebrating',
            name='wikipedia',
            endpoint=d.celebration.wiki_html,
            media_type='text/html',
            external=True
        ))
        self.add_link(Link(
            rel='repcal:celebrating',
            name='wikipedia-api',
            endpoint=d.celebration.wiki_json,
            media_type='application/json',
            external=True
        ))
