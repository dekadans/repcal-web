API Documentation
=================

The API that powers Repcal.info is available for anyone free of charge and without authentication.

It is designed around hypermedia principles using
[JSON Hypertext Application Language (HAL)](https://datatracker.ietf.org/doc/html/draft-kelly-json-hal)
as the primary media type.

_Hypermedia_ in this context means that interaction with the API is done using client selection
of server-provided choices, i.e. using the application by following links from one resource to another.
The relationship between two linked resources is described by the _link relation type_
(as defined by [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288.html)).

This API has defined a handful of [custom link relation types](/meta/relation),
but also use ones that are registered with IANA, like `describedby` which in this API will link to
[JSON schemas](https://json-schema.org/) for all API resources.

Entry Point
-----------

The [index resource (/api)](/api) serves as the entry point to navigating the API and
lists available operations and resources.

**Example:** Resolving the `repcal:now` link in the index resource will return
representations of the current date and time.

CLI Tool
--------

In addition to this website and API there's also [repcal](https://github.com/dekadans/repcal)
the CLI application (and Python library) for doing basic calendar and time related conversions.

Issues
------

Problems with this website or API can be reported on its [Github repository](https://github.com/dekadans/repcal-web).