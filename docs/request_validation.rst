Request validation
==================

This library uses Pydantic models to validate and serialize request payloads before sending
them to the wFirma API.

General rule
------------

For **all resource actions that send data** (especially ``add`` and ``edit``), the payload must
be validated with Pydantic **before** the HTTP request is sent.

This works in two modes:

1. **Typed input (preferred)**

   If a method receives a correct Pydantic model instance (for example a payload model dedicated
   to a given resource), it is used as-is.

2. **Untyped input (convenience)**

   If a method receives a plain mapping / keyword arguments, it is validated via
   ``YourModel.model_validate(...)``.

After validation, the payload is serialized using Pydantic (typically
``model_dump(mode="json")``) and then sent to the API.

What validation does (and does not) guarantee
---------------------------------------------

* Validation guarantees that **types and allowed values** match the library's contract.
  For example: correct enums, decimals, optional fields, forbidden extras.

* Validation does **not** guarantee that the wFirma API will accept a request.
  The API can still reject payloads due to business rules, permissions, server-side state,
  undocumented constraints, or discrepancies in the upstream documentation.

However, if the integration layer and payload structures are implemented according to the
public wFirma API documentation, then the library has done everything required on its side:

* It produced a correctly shaped payload.
* It validated that payload.
* It serialized it into the expected transport format.

At this point, an API rejection is outside the library's responsibility.

Practical example
-----------------

A simplified pattern used by resource methods::

    payload_model = PayloadModel.model_validate({"field": "value"})
    payload = payload_model.model_dump(mode="json")
    data = client.post_json("/resource/add", data=payload)


