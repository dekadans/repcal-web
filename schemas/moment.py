from . import link


def schema():
    return {
        "title": "Moment",
        "type": "object",
        "description": "A specific point in time.",
        "properties": {
            "_links": {
                "type": "object",
                "required": [
                    "self",
                    "describedby"
                ],
                "properties": {
                    "self": {
                        "$ref": link.url()
                    },
                    "describedby": {
                        "$ref": link.url()
                    },
                    "curies": {
                        "type": "array",
                        "items": {
                            "$ref": link.url()
                        }
                    },
                    "resource:date": {
                        "$ref": link.url()
                    },
                    "resource:time": {
                        "$ref": link.url()
                    }
                }
            },
            "iso": {
                "type": "string",
                "format": "date-time",
                "description": "ISO 8601 representation of the Moment."
            }
        },
        "required": [
            "_links",
            "iso"
        ]
    }