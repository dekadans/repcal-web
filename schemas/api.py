from . import link


def schema():
    return {
        "title": "ApiIndex",
        "type": "object",
        "description": "Hypermedia index of the API, offering links to resources and operations.",
        "properties": {
            "_links": link.schema([
                "service-doc",
                "repcal:now",
                "repcal:date",
                "repcal:time",
                "repcal:ui",
                "curies"
            ])
        },
        "required": [
            "_links"
        ]
    }