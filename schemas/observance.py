from . import link

def schema():
    return {
        "title": "Observance",
        "type": "object",
        "description": "Information about the observance or celebration of a particular day.",
        "properties": {
            "_links": link.schema(["curies", "repcal:wiki"]),
            "texts": {
                "type": "object",
                "required": [
                    "default",
                    "tagged"
                ],
                "properties": {
                    "default": {
                        "type": "string",
                        "description": "Text describing the observance."
                    },
                    "tagged": {
                        "type": "string",
                        "description": "The default text but structured with XML tags."
                    }
                }
            },
            "attributes": {
                "type": "object",
                "required": [
                    "month",
                    "day"
                ],
                "properties": {
                    "month": {
                        "type": "object",
                        "required": [
                            "id",
                            "name"
                        ],
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Wikidata entity ID"
                            },
                            "name": {
                                "type": "string",
                                "description": "The natural phenomenon this month was named for."
                            }
                        }
                    },
                    "day": {
                        "type": "object",
                        "required": [
                            "id",
                            "name"
                        ],
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Wikidata entity ID"
                            },
                            "name": {
                                "type": "string",
                                "description": "Name of the plant, animal, object or concept that this day is commemorating."
                            }
                        }
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