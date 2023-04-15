from datetime import datetime
from typing import Dict

from flask import jsonify

from .links import Link, Curie
from .resources import Resource, Date, Time, Moment, ApiIndex


class HALResponse:
    def __init__(self, primary: Resource) -> None:
        self.primary: Resource = primary
        self.embedded: Dict[str, Resource] = {}
        self.links = {}
        self.add_link(self._get_resource_link('self', self.primary))
        self.add_link(Link(
            rel='describedby',
            endpoint='meta.schema_'+self.primary.type(),
            media_type='application/schema+json'
        ))

    def _get_resource_link(self, rel: str, r: Resource) -> Link:
        return Link(
            rel=rel,
            endpoint="{}_resource".format(r.type()),
            media_type='application/hal+json',
            params=r.params()
        )

    def add_embedded(self, key: str, value: Resource) -> None:
        self.embedded[key] = value
        self.add_link(self._get_resource_link(key, value))

    def add_curie(self, link: Curie) -> None:
        if 'curies' not in self.links:
            self.links['curies'] = []
        self.links['curies'].append(link.parse())

    def add_link(self, link: Link) -> None:
        if link.rel not in self.links:
            self.links[link.rel] = link.parse()
            return

        if type(self.links[link.rel]) is dict:
            self.links[link.rel] = [self.links[link.rel]]

        self.links[link.rel].append(link.parse())

    def to_dict(self) -> dict:
        resp = {
            '_links': self.links,
            **self.primary.to_dict()
        }

        if len(self.embedded) > 0:
            resp['_embedded'] = {key: HALResponse(value).to_dict() for (key, value) in self.embedded.items()}

        return resp

    def to_response(self):
        resp = jsonify(self.to_dict())
        resp.content_type = "application/hal+json"
        return resp


class MomentResponse(HALResponse):
    def __init__(self, dt: datetime) -> None:
        super().__init__(Moment(dt))

        self.add_curie(Curie('repcal'))
        self.add_embedded('repcal:date', Date(dt.date()))
        self.add_embedded('repcal:time', Time(dt.time()))


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

