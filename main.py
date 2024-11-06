import re
from datetime import datetime, timezone, timedelta, date, time

from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, BadRequest, NotFound

from . import errors, meta, resources, responses

app = Flask(__name__)
app.register_blueprint(errors.bp)
app.register_blueprint(meta.bp)
app.json.sort_keys = False
CORS(app)


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/convert')
def convert():
    return render_template('details.html')


@app.get('/api')
def apiindex_resource():
    resp = responses.make_response(resources.ApiIndex()).to_response()
    resp.headers.add("Cache-Control", "max-age=3600, public")
    return resp


@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.get('/now')
def now_lookup():
    offset = Offset(request.args.get('offset', '0'))
    t = datetime.now(timezone.utc).timestamp()
    return redirect(url_for('moment_resource', timestamp=int(t), offset=str(offset)))


@app.get('/now{?offset}')
def now_template():
    raise NotFound()


@app.get('/moment/<int:timestamp>/<string:offset>')
def moment_resource(timestamp: int, offset: str):
    if timestamp > 6996800000:
        raise BadRequest('Timestamp out of bounds')

    offset = Offset(offset)
    tz = timezone(offset.to_timedelta())
    dt = datetime.fromtimestamp(timestamp, tz)
    r = resources.Moment(dt)
    return responses.make_response(r, ['repcal:observance']).to_response()


@app.get('/date/<int:year>/<int:month>/<int:day>')
def date_resource(year, month, day):
    # Max date
    try:
        d = date(year, month, day)
        r = resources.Date(d)
        return responses.make_response(r).to_response()
    except ValueError:
        raise NotFound('This URI does not correspond to a valid Date resource.')


@app.get('/date{/year:4,month:2,day:2}')
def date_template():
    raise NotFound()


@app.get('/time/<int:hour>/<int:minute>/<int:second>')
def time_resource(hour, minute, second):
    try:
        t = time(hour, minute, second)
        dt = resources.Time(t)
        return responses.make_response(dt).to_response()
    except ValueError:
        raise NotFound('This URI does not correspond to a valid Time resource.')


@app.get('/time{/hour:2,minute:2,second:2}')
def time_template():
    raise NotFound()


@app.get('/observance/<int:index>')
def observance_resource(index):
    try:
        obs = resources.Observance(index)
        return responses.make_response(obs).to_response()
    except IndexError:
        raise NotFound('This URI does not correspond to a valid Observance resource.')


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return errors.make_error_response(e)


class Offset:
    def __init__(self, offset: str) -> None:
        self.min = 0
        self._extract(offset)

    def to_timedelta(self) -> timedelta:
        return timedelta(minutes=self.min)

    def __str__(self) -> str:
        return str(self.min)

    def _extract(self, offset: str):
        result = re.match('^(-?\d{1,4})$', offset)
        if result is None:
            raise BadRequest('The provided offset was invalid or out-of-bounds.')

        self._set_minutes(result.group(1))

    def _set_minutes(self, minutes):
        if minutes is None:
            return

        minutes = int(minutes)
        if not -1440 < minutes < 1440:
            raise BadRequest('The provided offset was invalid or out-of-bounds.')

        self.min = minutes
