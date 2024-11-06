def make_response(resource, embeds=None):
    if embeds is None:
        embeds = []

    from ..resources import ApiIndex, Date, Moment, Observance

    if isinstance(resource, ApiIndex):
        from . import ApiIndexResponse
        return ApiIndexResponse(resource)
    elif isinstance(resource, Moment):
        from . import MomentResponse
        return MomentResponse(resource, embeds)
    elif isinstance(resource, Date):
        from . import DateResponse
        return DateResponse(resource, embeds)
    elif isinstance(resource, Observance):
        from . import ObservanceResponse
        return ObservanceResponse(resource, embeds)
    else:
        from . import HALResponse
        return HALResponse(resource, embeds)
