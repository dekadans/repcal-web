from .HALResponse import HALResponse
from ..resources import Observance
from .links import Curie, Link


class ObservanceResponse(HALResponse):
    def __init__(self, o: Observance, e) -> None:
        super().__init__(o, e)

        self.add_link(Curie('repcal'))

        rel = 'repcal:wiki'

        self.add_link(Link(
            rel=rel,
            name='day',
            endpoint=o.day.wiki_html,
            media_type='text/html',
            external=True
        ))

        self.add_link(Link(
            rel=rel,
            name='month',
            endpoint=o.month.wiki_html,
            media_type='text/html',
            external=True
        ))
