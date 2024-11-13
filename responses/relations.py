
class Relation:
    def __init__(self, media_type: str, resource: str, text: str, used_by: list[str], has_schema: bool = False):
        self.media_type = media_type
        self.resource = resource
        self.has_schema = has_schema
        self.used_by = used_by
        self.text = text


class HALRelation(Relation):
    def __init__(self, resource: str, text: str, used_by: list[str]):
        super().__init__(
            'application/hal+json',
            resource,
            text,
            used_by,
            True
        )


class Now(HALRelation):
    def __init__(self):
        super().__init__(
            'moment',
            """Link that will resolve to a resource representing the current date and time in the French Republican style.
            The <small><code>offset</code></small> query parameter can optionally be used to communicate the number of minutes from UTC.""",
            ['ApiIndex']
        )


class Date(HALRelation):
    def __init__(self):
        super().__init__(
            'date',
            """Link to a resource representing a date.
            May be to a specific resource relating to the link context, or templated for generic usage.""",
            ['ApiIndex', 'Moment']
        )


class Observance(HALRelation):
    def __init__(self):
        super().__init__(
            'observance',
            'Link to a resource describing observances or celebrations related to the link context.',
            ['Date']
        )


class Time(HALRelation):
    def __init__(self):
        super().__init__(
            'time',
            """Link to a resource representing time.
            May be to a specific resource relating to the link context, or templated for generic usage.""",
            ['ApiIndex', 'Moment']
        )


class Transform(Relation):
    def __init__(self):
        super().__init__(
            'application/xml',
            'XSLT Stylesheet document',
            text='Link to an XSL transformation resource used when rendering the repcal.info UI.',
            used_by=['ApiIndex']
        )


class Wikipedia(Relation):
    def __init__(self):
        super().__init__(
            'text/html',
            'website',
            text="""External link to an article on Wikipedia relating to the link context.""",
            used_by=['Observance']
        )
