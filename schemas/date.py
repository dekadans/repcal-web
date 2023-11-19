from . import link


def schema():
    return {
        "title": "Date",
        "type": "object",
        "description": "Date information in the French Republican style.",
        "properties": {
            "_links": link.schema(),
            "texts": {
                "type": "object",
                "required": [
                    "default"
                ],
                "properties": {
                    "default": {
                        "type": "string",
                        "description": "The default text representation of this date."
                    }
                }
            },
            "attributes": {
                "type": "object",
                "required": [
                    "complementary",
                    "day",
                    "week",
                    "month",
                    "year"
                ],
                "properties": {
                    "complementary": {
                        "type": "boolean",
                        "description": "True if we're in the end-of-year complementary days."
                    },
                    "day": {
                        "type": "object",
                        "required": [
                            "name",
                            "number_in_week",
                            "number_in_month"
                        ],
                        "description": "Information about this date's day.",
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "number_in_week": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10
                            },
                            "number_in_month": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 30
                            }
                        }
                    },
                    "week": {
                        "type": [
                            "object",
                            "null"
                        ],
                        "description": "Information about this date's week. NULL if we're in complementary days.",
                        "required": [
                            "number_in_month",
                            "number_in_year"
                        ],
                        "properties": {
                            "number_in_month": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 3
                            },
                            "number_in_year": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 36
                            }
                        }
                    },
                    "month": {
                        "type": [
                            "object",
                            "null"
                        ],
                        "description": "Information about this date's month. NULL if we're in complementary days.",
                        "required": [
                            "name",
                            "number"
                        ],
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "number": {
                                "type": "number",
                                "minimum": 1,
                                "maximum": 12
                            }
                        }
                    },
                    "year": {
                        "type": "object",
                        "required": [
                            "arabic",
                            "roman"
                        ],
                        "description": "Information about this date's year.",
                        "properties": {
                            "arabic": {
                                "type": "integer"
                            },
                            "roman": {
                                "type": "string"
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
