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
                "description": "ISO 8601 representation of the point in time."
            },
            "_embedded": {
                "type": "object",
                "required": [
                    "repcal:date",
                    "repcal:time"
                ],
                "description": "Embedded date and time resources."
            }
        },
        "required": [
            "_links",
            "_embedded",
            "iso"
        ]
    }