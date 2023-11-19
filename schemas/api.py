from . import link


def schema():
    return {
        "title": "ApiIndex",
        "type": "object",
        "description": "Hypermedia index of the API, offering links to useful resources.",
        "properties": {
            "_links": link.schema(),
            "name": {
                "type": "string",
                "description": "API name."
            },
            "description": {
                "type": "string",
                "description": "Short API description."
            }
        },
        "required": [
            "_links",
            "name",
            "description"
        ]
    }