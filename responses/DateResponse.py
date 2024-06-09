from .HALResponse import HALResponse
from ..resources import Date
from .links import Curie, Link


class DateResponse(HALResponse):
    def __init__(self, d: Date) -> None:
        super().__init__(d)

        self.add_curie(Curie('repcal'))

        rel = 'repcal:wiki'

        self.add_link(Link(
            rel=rel,
            name='day',
            endpoint=d.day_entity.wiki_html,
            media_type='text/html',
            external=True
        ))

        self.add_link(Link(
            rel=rel,
            name='month',
            endpoint=d.month_entity.wiki_html,
            media_type='text/html',
            external=True
        ))
