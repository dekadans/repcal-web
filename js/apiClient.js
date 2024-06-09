async function getNow() {
    const offset = (new Date()).getTimezoneOffset() * -1;
    const response = await fetch('/now?offset=' + offset);
    const data = await response.json();

    return {
        ...parseDate(data._embedded['repcal:date']),
        ...parseTime(data._embedded['repcal:time'])
    };
}

async function convertDate(dateString) {
    const [year, month, date] = dateString.split('-');
    const response = await fetch(`/date/${year}/${month}/${date}`);
    const data = await response.json();
    return parseDate(data);
}

function parseDate(api_date) {
    const uiLink = api_date
        ._links['repcal:meta-day']
        .find(l => l.name === 'ui');

    return {
        date: api_date.texts.default,
        celebrating: uiLink.title,
        wiki: uiLink.href
    }
}

function parseTime(api_time) {
    return {
        hour: api_time.attributes.hour,
        minute: api_time.attributes.minute,
        second: api_time.attributes.second
    };
}

export {
    getNow,
    convertDate
}