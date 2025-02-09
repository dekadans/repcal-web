from flask import Blueprint, jsonify, url_for, render_template, send_file
from werkzeug.exceptions import NotFound
from .schemas import api, moment, time, date, observance, link
from .responses import relations

bp = Blueprint('meta', __name__, url_prefix='/meta')


@bp.get('/service/doc')
def service_doc():
    return send_file('schemas/api.md', 'text/markdown')


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


@bp.get('/schema/observance')
def schema_observance():
    return schema_response(observance.schema())


def schema_response(data):
    name = data['title'].lower()
    r = jsonify({
        '$schema': 'https://json-schema.org/draft/2019-09/schema',
        '$id': url_for(f'meta.schema_{name}', _external=True),
        **data,
        **link.link_def()
    })
    r.content_type = 'application/schema+json'
    return r


@bp.get('/relation')
def relation_index():
    return render_template('relation.html', name=None, info=None)

@bp.get('/relation/{rel}')
def relation_template():
    raise NotFound()


@bp.get('/relation/<string:rel>')
def relation(rel: str):
    rels = {
        'now': relations.Now,
        'date': relations.Date,
        'observance': relations.Observance,
        'time': relations.Time,
        'wiki': relations.Wikipedia,
        'ui': relations.UI
    }

    if rel in rels:
        return render_template('relation.html', name=rel, info=rels[rel]())
    else:
        raise NotFound()


@bp.get('/transform/observance')
def transform_observance():
    return send_file('observance/observance.xslt', 'application/xml')
