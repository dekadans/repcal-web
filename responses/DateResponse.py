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
            endpoint='https://en.wikipedia.org/wiki/' + d.celebration.wiki_id,
            media_type='text/html',
            external=True
        ))
        self.add_link(Link(
            rel='repcal:celebrating',
            name='wikipedia-api',
            endpoint='https://en.wikipedia.org/api/rest_v1/page/summary/' + d.celebration.wiki_id,
            media_type='application/json',
            external=True
        ))
