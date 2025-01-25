API Documentation
=================

The API that powers Repcal.info is available for anyone free of charge and without authentication.

It is designed around hypermedia principles using
[JSON Hypertext Application Language (HAL)](https://datatracker.ietf.org/doc/html/draft-kelly-json-hal)
as the primary media type. _Hypermedia_ in this context means that the client interacts with the application by following links
provided by the server.

Index Resource
--------------

The [index resource (/api)](/api) serves as the entry point to navigating the API and 
links to available operations and resources.

Link Relation
-------------

The relationship between two linked resources is described by the _link relation type_
(as defined by [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288.html)).

This API has defined a handful of [custom link relation types](/meta/relation),
but also use ones that are registered with IANA, like `describedby` which in this API will link to
[JSON schemas](https://json-schema.org/) for all API resources.

Under the Hood
-----------

The functionality seen on Repcal.info is implemented in two separate code repositories:

- [repcal](https://github.com/dekadans/repcal): The core date and time conversion functionality as a Python package and CLI tool. 
- [repcal-web](https://github.com/dekadans/repcal-web): This website and API as well as observational data for each day and month.

Both applications are published under the MIT license.
Problems or suggestions can be submitted as issues to the appropriate repository.

Repcal is maintained by [Tomas Thelander](https://tthe.se).