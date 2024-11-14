from urllib.parse import unquote

from flask import url_for


class Link:
    def __init__(self, rel: str, endpoint: str, media_type: str | None = 'application/hal+json', params=None,
                 external=False, to_many=False, **kwargs) -> None:
        self.rel = rel
        self.endpoint = endpoint
        self.media_type = media_type
        self.params = {} if params is None else params
        self.external = external
        self.to_many = to_many
        self.kwargs = kwargs

    def parse(self) -> dict:
        if self.external:
            href = self.endpoint
        else:
            href = url_for(self.endpoint, _external=True, **self.params)
            if self.kwargs.get('templated'):
                href = unquote(href)

        if self.media_type is not None:
            self.kwargs['type'] = self.media_type

        return {
            'href': href,
            **self.kwargs
        }


class Curie(Link):
    def __init__(self, name: str) -> None:
        super().__init__(
            rel='curies',
            endpoint='meta.relation_template',
            media_type='text/html',
            name=name,
            templated=True,
            to_many=True
        )
