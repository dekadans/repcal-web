from ..resources import Resource
from .links import Link
from typing import Dict, List
from flask import jsonify
from .factory import make_response


class HALResponse:
    def __init__(self, primary: Resource, requested_embeds) -> None:
        self.primary: Resource = primary
        self.requested_embeds: List = requested_embeds
        self.embedded: Dict[str, Resource] = {}
        self.links = {}
        self.add_link(self._get_resource_link('self', self.primary))
        self.add_link(Link(
            rel='describedby',
            endpoint='meta.schema_' + self.primary.type(),
            media_type='application/schema+json'
        ))
        self.is_embedded = False

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

    def add_link(self, link: Link) -> None:
        parsed_link = link.parse()

        if link.rel not in self.links:
            self.links[link.rel] = parsed_link if not link.to_many else [parsed_link]
            return

        if type(self.links[link.rel]) is dict:
            self.links[link.rel] = [self.links[link.rel]]

        self.links[link.rel].append(parsed_link)

    def to_dict(self) -> dict:
        if self.is_embedded and 'curies' in self.links:
            del self.links['curies']

        resp = {
            '_links': self.links,
            **self.primary.to_dict()
        }

        if len(self.embedded) > 0:
            resp['_embedded'] = {
                key: make_response(value, self.requested_embeds).as_embedded().to_dict()
                for (key, value) in self.embedded.items()
            }

        return resp

    def to_response(self):
        resp = jsonify(self.to_dict())
        resp.content_type = "application/hal+json"
        return resp

    def as_embedded(self):
        self.is_embedded = True
        return self
