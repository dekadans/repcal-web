from .HALResponse import HALResponse
from ..resources import Date
from .links import Curie, Link


class DateResponse(HALResponse):
    def __init__(self, d: Date) -> None:
        super().__init__(d)

        self.add_curie(Curie('repcal'))

        rel_observe = 'repcal:observation'

        self.add_link(Link(
            rel=rel_observe,
            name='entity',
            endpoint=d.celebration.uri,
            media_type=None,
            external=True
        ))
        self.add_link(Link(
            rel=rel_observe,
            name='ui',
            endpoint=d.celebration.wiki_html,
            media_type='text/html',
            external=True,
            hreflang='en',
            title=d.celebration.name
        ))
        self.add_link(Link(
            rel=rel_observe,
            name='data',
            endpoint=d.celebration.wiki_json,
            media_type='application/json',
            external=True,
            hreflang='en'
        ))
