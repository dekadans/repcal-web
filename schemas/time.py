from . import link


def schema():
    return {
        "title": "Time",
        "type": "object",
        "description": "Time information in the French Republican style.",
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
                    }
                }
            },
            "texts": {
                "type": "object",
                "required": [
                    "default",
                    "decimal"
                ],
                "properties": {
                    "default": {
                        "type": "string",
                        "description": "Default text representation of the time."
                    },
                    "decimal": {
                        "type": "string",
                        "description": "Time represented as a decimal number less than 1."
                    }
                }
            },
            "attributes": {
                "type": "object",
                "required": [
                    "hour",
                    "minute",
                    "second"
                ],
                "properties": {
                    "hour": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "The hour. Each day has 10 hours.",
                        "maximum": 9
                    },
                    "minute": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Minute. Each hour has 100 minutes.",
                        "maximum": 99
                    },
                    "second": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Second. Each minute has 100 seconds.",
                        "maximum": 99
                    }
                }
            }
        },
        "required": [
            "_links",
            "texts",
            "attributes"
        ]
    }
