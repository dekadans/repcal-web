from ..resources import ApiIndex
from .links import Link, Curie
from .HALResponse import HALResponse


class ApiIndexResponse(HALResponse):
    def __init__(self, i: ApiIndex) -> None:
        super().__init__(i)
        self.add_curie(Curie('repcal'))
        self.add_link(Link(
            rel='help',
            endpoint='https://datatracker.ietf.org/doc/html/draft-kelly-json-hal',
            media_type='text/html',
            title='Information about the HAL (Hypertext Application Language) JSON media type',
            external=True
        ))
        self.add_link(Link(
            rel='service-desc',
            endpoint='meta.openapi',
            media_type='application/openapi+yaml;version=3.1',
            title='OpenAPI description document'
        ))
        self.add_link(Link(
            rel='service-doc',
            endpoint='docs',
            media_type='text/html',
            title='Rendered API documentation'
        ))
        self.add_link(Link(
            rel='repcal:now',
            endpoint='now_template',
            title='Get the current date and time in the French republican systems',
            templated=True
        ))
        self.add_link(Link(
            rel='repcal:date',
            endpoint='date_template',
            title='Resolve a date to its French Republican counterpart.',
            templated=True
        ))
        self.add_link(Link(
            rel='repcal:time',
            endpoint='time_template',
            title='Resolve a time of day to its decimal counterpart.',
            templated=True
        ))

