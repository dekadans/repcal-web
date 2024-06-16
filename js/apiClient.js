import {parseTemplate} from "url-template";

const rel = {
    NOW: 'repcal:now',
    DATE: 'repcal:date',
    TIME: 'repcal:time',
    WIKI: 'repcal:wiki',
    TRANSFORM: 'repcal:transform'
};

const api = fetch('/api')
    .then(response => response.json())
    .then(data => data['_links']);

async function call(relation, params) {
    const relations = await api;
    const link = relations[relation];
    const uri = link.templated ? parseTemplate(link.href).expand(params) : link.href;
    const response = await fetch(uri);

    if (link.type.includes('json')) {
        return response.json();
    } else {
        return response.text();
    }
}

async function getNow() {
    const offset = (new Date()).getTimezoneOffset() * -1;
    const data = await call(rel.NOW, {offset});
    const resources = data['_embedded'];

    return {
        ...parseDate(resources[rel.DATE]),
        ...parseTime(resources[rel.TIME])
    };
}

/*
 * Takes a date in the format "2024-01-01"
 */
async function convertDate(dateString) {
    const [year, month, day] = dateString.split('-');
    const data = await call(rel.DATE, {year, month, day});
    return parseDate(data);
}

/*
 * Takes a timestamp in the format "00:00:00"
 */
async function convertTime(timeString) {
    const [hour, minute, second] = timeString.split(':');
    const data = await call(rel.TIME, {hour, minute, second});
    return parseTime(data);
}

function parseDate(api_date) {
    const wikiLinks = api_date['_links'][rel.WIKI];

    const dayLink = wikiLinks.find(l => l.name === 'day').href;
    const monthLink = wikiLinks.find(l => l.name === 'month').href;

    return {
        date: api_date.texts.default,
        dateShort: api_date.texts.short,
        observance: api_date.texts.observance.tagged,
        dayLink,
        monthLink
    }
}

function parseTime(api_time) {
    return {
        hour: api_time.attributes.hour,
        minute: api_time.attributes.minute,
        second: api_time.attributes.second
    };
}

async function getObservanceTransform() {
    return call(rel.TRANSFORM, null);
}

export {
    getNow,
    convertDate,
    convertTime,
    getObservanceTransform
}