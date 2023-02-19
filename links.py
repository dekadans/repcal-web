from urllib.parse import unquote

from flask import url_for
from werkzeug.exceptions import NotFound


class Link:
    def __init__(self, rel: str, endpoint: str, media_type: str = 'application/hal+json', params=None,
                 **kwargs) -> None:
        self.rel = rel
        self.endpoint = endpoint
        self.media_type = media_type
        self.params = {} if params is None else params
        self.kwargs = kwargs

    def parse(self):
        href = url_for(self.endpoint, _external=True, **self.params)
        if self.kwargs.get('templated'):
            href = unquote(href)

        return {
            'href': href,
            'type': self.media_type,
            **self.kwargs
        }


class Curie(Link):
    def __init__(self, name: str) -> None:
        super().__init__(
            rel='',
            endpoint='meta.relation_template',
            media_type='text/html',
            name=name,
            templated=True
        )
