from .HALResponse import HALResponse
from ..resources import Date
from .links import Curie, Link
from ..metadata import find_observation, find_month


class DateResponse(HALResponse):
    def __init__(self, d: Date) -> None:
        super().__init__(d)

        self.add_curie(Curie('repcal'))

        links = {
            'repcal:meta-day': find_observation(d.republican),
            'repcal:meta-month': find_month(d.republican)
        }

        for rel, subject in links.items():
            self.add_link(Link(
                rel=rel,
                name='entity',
                endpoint=subject.uri,
                media_type=None,
                external=True
            ))
            self.add_link(Link(
                rel=rel,
                name='ui',
                endpoint=subject.wiki_html,
                media_type='text/html',
                external=True,
                hreflang='en',
                title=subject.name
            ))
            self.add_link(Link(
                rel=rel,
                name='data',
                endpoint=subject.wiki_json,
                media_type='application/json',
                external=True,
                hreflang='en'
            ))
