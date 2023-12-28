from flask import Blueprint, jsonify, url_for, render_template, send_file
from werkzeug.exceptions import NotFound
from .schemas import api, moment, time, date

bp = Blueprint('meta', __name__, url_prefix='/meta')


@bp.get('/openapi')
def openapi():
    return send_file('schemas/openapi.yaml', 'application/openapi+yaml;version=3.1')


@bp.get('/schema/api')
def schema_apiindex():
    return schema_response(api.schema())


@bp.get('/schema/moment')
def schema_moment():
    return schema_response(moment.schema())


@bp.get('/schema/time')
def schema_time():
    return schema_response(time.schema())


@bp.get('/schema/date')
def schema_date():
    return schema_response(date.schema())


def schema_response(data):
    name = data['title'].lower()
    r = jsonify({
        '$schema': 'https://json-schema.org/draft/2019-09/schema',
        '$id': url_for(f'meta.schema_{name}', _external=True),
        **data
    })
    r.content_type = 'application/schema+json'
    return r


@bp.get('/relation/{rel}')
def relation_template():
    raise NotFound()


@bp.get('/relation/<string:rel>')
def relation(rel: str):
    rels = {
        'now': 'The <em>now</em> link will resolve to a resource representing the current date and time.',
        'date': 'This link will resolve to a related <em>date</em> resource.',
        'time': 'This link will resolve to a related <em>time</em> resource.',
        'celebrating': 'Link to additional information about the day\'s celebrations.'
    }

    if rel in rels:
        return render_template('relation.html', name=rel, text=rels[rel])
    else:
        raise NotFound()

