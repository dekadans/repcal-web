from ..resources import ApiIndex
from .links import Link, Curie
from .HALResponse import HALResponse


class ApiIndexResponse(HALResponse):
    educational = [
        ('HAL - Hypertext Application Language', 'https://datatracker.ietf.org/doc/html/draft-kelly-json-hal'),
        ('JSON Schema', 'https://json-schema.org/'),
        ('OpenAPI', 'https://www.openapis.org/'),
        ('RFC 7807 - Problem Details for HTTP APIs', 'https://www.rfc-editor.org/rfc/rfc7807')
    ]

    def __init__(self) -> None:
        super().__init__(ApiIndex())
        self.add_curie(Curie('repcal'))
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

        for title, url in self.educational:
            self.add_link(Link(
                rel='repcal:educational',
                endpoint=url,
                title=title,
                media_type='text/html',
                external=True
            ))

