from . import link


def schema():
    return {
        "title": "ApiIndex",
        "type": "object",
        "description": "Hypermedia index of the API, offering links to useful resources.",
        "properties": {
            "_links": {
                "type": "object",
                "required": [
                    "self",
                    "describedby"
                ],
                "properties": {
                    "self": {
                        "$ref": link.url(),
                        "description": "The URI of this resource."
                    },
                    "describedby": {
                        "$ref": link.url(),
                        "description": "The describedby relation provides JSON Schema context about the resource."
                    },
                    "curies": {
                        "type": "array",
                        "description": "\"Compact URIs\", a way of shortening extension relation types.",
                        "items": {
                            "$ref": link.url()
                        }
                    },
                    "service-desc": {
                        "$ref": link.url(),
                        "description": "Machine-readable service description (RFC 8631)."
                    },
                    "service-doc": {
                        "$ref": link.url(),
                        "description": "URI for human-readable service description (RFC 8631)."
                    },
                    "repcal:now": {
                        "$ref": link.url(),
                        "description": "Get the current (republican) date and time."
                    },
                    "repcal:educational": {
                        "type": "array",
                        "description": "A list of links to specifications and technologies used when implementing this API.",
                        "items": {
                            "$ref": link.url()
                        }
                    }
                }
            },
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