from datetime import datetime
from typing import Dict

from links import Link, Curie
from resources import Resource, Date, Time, Moment, ApiIndex


class HALResponse:
    def __init__(self, primary: Resource) -> None:
        self.primary: Resource = primary
        self.embedded: Dict[str, Resource] = {}
        self.links = {}
        self.add_link(self._get_resource_link('self', self.primary))
        self.add_link(Link(
            rel='describedby',
            endpoint='meta.schema',
            media_type='application/schema+json',
            params={'name': self.primary.type()}
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
        self.links[link.rel] = link.parse()

    def to_dict(self) -> dict:
        resp = {
            '_links': self.links,
            **self.primary.to_dict()
        }

        if len(self.embedded) > 0:
            resp['_embedded'] = {key: HALResponse(value).to_dict() for (key, value) in self.embedded.items()}

        return resp


class MomentResponse(HALResponse):
    def __init__(self, dt: datetime) -> None:
        super().__init__(Moment(dt))

        self.add_curie(Curie('resource'))
        self.add_embedded('resource:date', Date(dt.date()))
        self.add_embedded('resource:time', Time(dt.time()))


class ApiIndexResponse(HALResponse):
    def __init__(self) -> None:
        super().__init__(ApiIndex())
        self.add_curie(Curie('operation'))
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
            rel='operation:now',
            endpoint='now_template',
            title='Get the current date and time in the French republican systems',
            templated=True
        ))
        self.add_link(Link(
            rel='operation:paris',
            endpoint='paris_lookup',
            title='Get the current Paris Mean date and time'
        ))

