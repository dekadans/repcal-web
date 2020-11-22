from flask import Flask, render_template, request
from repcal import RepublicanDate, DecimalTime
from datetime import datetime, timezone, timedelta
import json
from werkzeug.exceptions import HTTPException, BadRequest

app = Flask(__name__)


@app.route('/')
def test():
    return render_template('index.html')


@app.route('/now.json')
def now_json():
    tz = get_timezone()
    now = datetime.now(tz)
    return make_response(now)


@app.route('/<int:timestamp>.json')
def timestamp_json(timestamp):
    if timestamp > 6996800000:
        raise BadRequest('Timestamp out of bounds')

    tz = get_timezone()
    dt = datetime.fromtimestamp(timestamp, tz)
    return make_response(dt)


def get_timezone():
    offset = request.args.get('offset', '0')

    if not offset.lstrip('-').isdigit():
        raise BadRequest('Invalid offset')

    offset = int(offset)

    try:
        tz = timezone(timedelta(minutes=offset))
    except ValueError:
        raise BadRequest('Invalid offset')

    return tz


def make_response(d):
    rep_date = RepublicanDate.from_gregorian(d.date())
    dec_time = DecimalTime.from_standard_time(d.time())

    rep_date_str = str(rep_date)
    rep_date_str = rep_date_str[0].upper() + rep_date_str[1:]

    return {
        "republican_date": {
            "attributes": {
                "year_arabic": rep_date.get_year_arabic(),
                "year_roman": rep_date.get_year_roman(),
                "month": rep_date.get_month(),
                "week": rep_date.get_week_number(),
                "weekday": rep_date.get_weekday(),
                "day": rep_date.get_day(),
                "sansculottides": rep_date.is_sansculottides()
            },
            "formatted": rep_date_str
        },
        "decimal_time": {
            "attributes": {
                "hour": dec_time.hour,
                "minute": dec_time.minute,
                "second": dec_time.second
            },
            "formatted": str(dec_time)
        },
        "standard": {
            "timestamp": d.timestamp(),
            "utc_offset_minutes": int(d.utcoffset().total_seconds() // 60),
            "formatted": d.isoformat()
        }
    }


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
