from datetime import datetime, timezone, timedelta, date, time
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.exceptions import HTTPException, BadRequest, NotFound

import errors
import meta
import resources
import responses

app = Flask(__name__)
app.register_blueprint(errors.bp)
app.register_blueprint(meta.bp)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def start():
    return render_template('index.html')


@app.get('/api')
def api_resource():
    return responses.ApiIndexResponse().to_dict()


@app.route('/docs')
def docs():
    return 'docs'


@app.get('/now')
def now_lookup():
    offset = _get_offset(request.args.get('offset', '0'))
    t = datetime.now(timezone.utc).timestamp()
    return redirect(url_for('moment_resource', timestamp=int(t), offset=offset))


@app.get('/now{?offset}')
def now_template():
    raise NotFound()


@app.get('/moment/<int:timestamp>/<string:offset>')
def moment_resource(timestamp: int, offset: str):
    if timestamp > 6996800000:
        raise BadRequest('Timestamp out of bounds')

    offset = _get_offset(offset)
    tz = timezone(timedelta(minutes=offset))
    dt = datetime.fromtimestamp(timestamp, tz)
    return responses.MomentResponse(dt).to_dict()


@app.get('/date/<int:year>/<int:month>/<int:day>')
def date_resource(year, month, day):
    # Max date
    try:
        d = date(year, month, day)
        r = resources.Date(d)
        return responses.HALResponse(r).to_dict()
    except ValueError:
        raise NotFound('This URI does not correspond to a valid Date resource.')


@app.get('/time/<int:hour>/<int:minute>/<int:second>')
def time_resource(hour, minute, second):
    try:
        t = time(hour, minute, second)
        dt = resources.Time(t)
        return responses.HALResponse(dt).to_dict()
    except ValueError:
        raise NotFound('This URI does not correspond to a valid Time resource.')


def _get_offset(offset: str) -> int:
    if not offset.lstrip('-').isdigit():
        raise errors.InvalidOffset()

    offset = int(offset)

    if not -1440 <= offset <= 1440:
        raise errors.InvalidOffset()

    return offset


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return errors.make_error_response(e)
