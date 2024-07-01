from . import link


def schema():
    return {
        "title": "ApiIndex",
        "type": "object",
        "description": "Hypermedia index of the API, offering links to resources and operations.",
        "properties": {
            "_links": link.schema()
        },
        "required": [
            "_links"
        ]
    }