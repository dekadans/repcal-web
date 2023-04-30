from flask import Blueprint, url_for, make_response
import json
import uuid

bp = Blueprint('errors', __name__, url_prefix='/meta/errors')


@bp.get('/<string:error_type>/<uuid:error_instance>')
def error(error_type, error_instance):
    resp = make_response("Hello! URIs are identifiers and doesn't have yield anything in particular when resolved "
                         "in a web browser.")
    resp.content_type = 'text/plain'
    return resp


def make_error_response(e):
    concept_uri = 'https://webconcepts.info/concepts/http-status-code/{}'.format(e.code)
    uri_instance = url_for('errors.error', error_type=e.code, error_instance=str(uuid.uuid4()), _external=True)

    response = e.get_response()
    response.data = json.dumps({
        "type": concept_uri,
        "instance": uri_instance,
        "status": e.code,
        "title": e.name,
        "detail": e.description,
    })
    response.content_type = "application/problem+json"
    return response
