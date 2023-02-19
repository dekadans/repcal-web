from flask import Blueprint
from werkzeug.exceptions import NotFound

bp = Blueprint('meta', __name__, url_prefix='/meta')


@bp.get('/openapi')
def openapi():
    return {}


@bp.get('/schema/<string:name>')
def schema(name: str):
    return {}


@bp.get('/relation/{rel}')
def relation_template():
    raise NotFound()


@bp.get('/relation/<string:rel>')
def relation(rel: str):
    return 'info about relation'

