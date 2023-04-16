from ..resources import Resource
from .links import Link, Curie
from typing import Dict
from flask import jsonify


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
