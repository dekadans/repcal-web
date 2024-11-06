
class Relation:
    def __init__(self, media_type: str, resource: str, text: str, has_schema: bool = False):
        self.media_type = media_type
        self.resource = resource
        self.has_schema = has_schema
        self.text = text


class HALRelation(Relation):
    def __init__(self, resource: str, text: str):
        super().__init__(
            'application/hal+json',
            resource,
            text,
            True
        )


class Now(HALRelation):
    def __init__(self):
        super().__init__(
            'moment',
            'This link will resolve to a moment resource representing the current date and time.'
        )


class Date(HALRelation):
    def __init__(self):
        super().__init__(
            'date',
            'This link will resolve to a date resource. May be to a specific resource or templated for generic usage.'
        )


class Observance(HALRelation):
    def __init__(self):
        super().__init__(
            'observance',
            'This link will resolve to an observance resource, linked from a date resource.'
        )


class Time(HALRelation):
    def __init__(self):
        super().__init__(
            'time',
            'This link will resolve to a time resource. May be to a specific resource or templated for generic usage.'
        )


class Transform(Relation):
    def __init__(self):
        super().__init__(
            'application/xml',
            'XSLT Stylesheet',
            text='Links to resources for XSL transformations.'
        )


class Wikipedia(Relation):
    def __init__(self):
        super().__init__(
            'text/html',
            'N/A (External)',
            text="""External links to Wikipedia."""
        )
