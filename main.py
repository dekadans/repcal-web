import re
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
    offset = Offset(request.args.get('offset', '0'))
    t = datetime.now(timezone.utc).timestamp()
    return redirect(url_for('moment_resource', timestamp=int(t), offset=str(offset)))


@app.get('/now{?offset}')
def now_template():
    raise NotFound()


@app.get('/paris')
def paris_lookup():
    offset = Offset('9.21')
    t = datetime.now(timezone.utc).timestamp()
    return redirect(url_for('moment_resource', timestamp=int(t), offset=str(offset)))


@app.get('/moment/<int:timestamp>/<string:offset>')
def moment_resource(timestamp: int, offset: str):
    if timestamp > 6996800000:
        raise BadRequest('Timestamp out of bounds')

    offset = Offset(offset)
    tz = timezone(offset.to_timedelta())
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


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return errors.make_error_response(e)


class Offset:
    def __init__(self, offset: str) -> None:
        self.min = 0
        self.sec = 0
        self._extract(offset)

    def to_timedelta(self) -> timedelta:
        return timedelta(minutes=self.min, seconds=self.sec)

    def __str__(self) -> str:
        s = str(self.min)
        if self.sec is not None and self.sec > 0:
            s += '.' + str(self.sec)
        return s

    def _extract(self, offset: str):
        result = re.match('^(-?\d{1,4})(?:\.(\d{1,2}))?$', offset)
        if result is None:
            raise errors.InvalidOffset()

        self._set_minutes(result.group(1))
        self._set_seconds(result.group(2))

    def _set_minutes(self, minutes):
        if minutes is None:
            return

        minutes = int(minutes)
        if not -1440 < minutes < 1440:
            raise errors.InvalidOffset()

        self.min = minutes

    def _set_seconds(self, seconds):
        if seconds is None:
            return

        seconds = int(seconds)
        if seconds > 59:
            raise errors.InvalidOffset()

        self.sec = seconds
