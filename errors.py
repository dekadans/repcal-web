from flask import Blueprint, url_for
import json
import uuid

from werkzeug.exceptions import BadRequest
from werkzeug.http import HTTP_STATUS_CODES

bp = Blueprint('errors', __name__, url_prefix='/meta/errors')


@bp.get('/<string:error_type>')
@bp.get('/<string:error_type>/<uuid:error_instance>')
def error(error_type, error_instance=None):
    if error_instance is not None:
        return 'instance'
    elif error_type.isdigit() and int(error_type) in HTTP_STATUS_CODES:
        return 'HTTP Status {}: {}'.format(error_type, HTTP_STATUS_CODES.get(int(error_type)))
    else:
        return 'Unknown error'


def make_error_response(e):
    try:
        error_type = e.error_type
    except AttributeError:
        error_type = e.code

    uri_type = url_for('errors.error', error_type=error_type, _external=True)
    uri_instance = url_for('errors.error', error_type=error_type, error_instance=str(uuid.uuid4()), _external=True)

    response = e.get_response()
    response.data = json.dumps({
        "type": uri_type,
        "instance": uri_instance,
        "status": e.code,
        "title": e.name,
        "detail": e.description,
    })
    response.content_type = "application/problem+json"
    return response


class InvalidOffset(BadRequest):
    error_type = 'invalid_offset'
    description = 'The provided offset was invalid or out-of-bounds.'
