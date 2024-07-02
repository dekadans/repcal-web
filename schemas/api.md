API Documentation
=================

Introduction
-----------

Lorem ipsum dolor sit amet consectetur adipiscing elit aptent tellus vitae,
curabitur praesent facilisis condimentum parturient hendrerit ultricies nisi placerat pellentesque,
massa dictumst inceptos felis eget nullam at tincidunt feugiat.

Curabitur fermentum vitae felis est consectetur congue fringilla tellus tempus nibh vivamus porta,
arcu pellentesque suscipit ullamcorper semper sodales magnis suspendisse ultricies curae.

### Quick Start

Test

Media Types
-----------

### HAL

* Media type: `application/hal+json`
* Learn more: [Internet-Draft - JSON Hypertext Application Language](https://datatracker.ietf.org/doc/html/draft-kelly-json-hal)

### JSON Schema

* Media type: `application/schema+json`
* Learn more: [JSON-Schema.org](https://json-schema.org/)

All HAL resources encountered in this API will have a `describedby` link to a JSON Schema describing it.
To improve their usefulness all schemas are rendered in a human-friendly way here: _todo_.

### Problem Details

* Media type: `application/problem+json`
* Learn more: [RFC 9457 - Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)

API Index
---------

* URI: [`/api`](/api)

Elementum leo litora pharetra maximus nulla justo hac, augue cursus nunc ullamcorper class accumsan,
porttitor nascetur faucibus dolor ultrices habitasse.


Link Relations
--------------

Listed below are link relation types, as defined by [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288.html),
that are used by this API:


* [`repcal:now`](/meta/relation/now)
* [`repcal:date`](/meta/relation/date)
* [`repcal:time`](/meta/relation/time)
* [`repcal:transform`](/meta/relation/transform)
* [`repcal:wiki`](/meta/relation/wiki)

Additionally, IANA-registered types like `self`, `describedby` and `service-doc` are also used.
