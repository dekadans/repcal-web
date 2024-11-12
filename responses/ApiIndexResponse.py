from ..resources import ApiIndex
from .links import Link, Curie
from .HALResponse import HALResponse


class ApiIndexResponse(HALResponse):
    def __init__(self, i: ApiIndex) -> None:
        super().__init__(i, [])
        self.add_link(Link(
            rel='service-doc',
            endpoint='meta.service_doc',
            media_type='text/markdown',
            title='API documentation markdown source.'
        ))
        self.add_link(Link(
            rel='repcal:now',
            endpoint='now_template',
            title='Get the current date and time in the French republican systems, optionally with UTC offset in minutes.',
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
        self.add_link(Link(
            rel='repcal:transform',
            endpoint='meta.transform_observance',
            title='Default HTML transformation for the tagged observance text.',
            name='observance',
            media_type='application/xml'
        ))
        self.add_curie(Curie('repcal'))

