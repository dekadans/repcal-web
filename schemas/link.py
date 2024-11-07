
def schema(requirements: list):
    return {
        "type": "object",
        "description": "Links in the format defined by the HAL JSON media type.",
        "required": [
            "self",
            "describedby",
            *requirements
        ],
        "additionalProperties": {
            "$ref": "#/$defs/one_or_many_links"
        }
    }

def link_def():
    return {
        "$defs": {
            "one_or_many_links": {
                "oneOf": [
                    {
                        "$ref": "#/$defs/hal_link"
                    },
                    {
                        "type": "array",
                        "items": {
                            "$ref": "#/$defs/hal_link"
                        }
                    }
                ]
            },
            "hal_link": {
                "type": "object",
                "required": [
                    "href"
                ],
                "properties": {
                    "href": {
                        "type": "string",
                        "format": "uri"
                    },
                    "type": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "templated": {
                        "type": "boolean"
                    }
                }
            }
        }
    }