from . import link


def schema():
    return {
        "title": "Moment",
        "type": "object",
        "description": "A specific point in time.",
        "properties": {
            "_links": link.schema(["curies", "repcal:date", "repcal:time"]),
            "iso": {
                "type": "string",
                "format": "date-time",
                "description": "ISO 8601 representation of the Moment."
            },
            "_embedded": {
                "type": "object",
                "description": "Embedded date and time resources."
            }
        },
        "required": [
            "_links",
            "_embedded",
            "iso"
        ]
    }