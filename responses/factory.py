def make_response(resource):
    from ..resources import ApiIndex, Date, Moment

    if isinstance(resource, ApiIndex):
        from . import ApiIndexResponse
        return ApiIndexResponse(resource)
    elif isinstance(resource, Moment):
        from . import MomentResponse
        return MomentResponse(resource)
    elif isinstance(resource, Date):
        from . import DateResponse
        return DateResponse(resource)
    else:
        from . import HALResponse
        return HALResponse(resource)
