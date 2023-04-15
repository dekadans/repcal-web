from flask import url_for


def url():
    return url_for('meta.schema_link')


def schema():
    return {
        "title": "Link",
        "description": "A hyperlink.",
        "type": "object",
        "properties": {
            "href": {
                "type": "string",
                "format": "uri",
                "description": "Target URI of the link"
            },
            "type": {
                "type": "string",
                "description": "Target media type"
            },
            "name": {
                "type": "string",
                "description": "Optional secondary key for identification among other links with the same relation."
            },
            "title": {
                "type": "string",
                "description": "Human-readable link title."
            },
            "templated": {
                "type": "boolean",
                "default": False
            }
        },
        "required": [
            "href",
            "type"
        ]
    }