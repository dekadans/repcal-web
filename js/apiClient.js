import {parseTemplate} from "url-template";

/*
 Link relations for defined operations and resources.
 */
const rel = {
    NOW: 'repcal:now',
    DATE: 'repcal:date',
    TIME: 'repcal:time',
    WIKI: 'repcal:wiki',
    TRANSFORM: 'repcal:transform',
    DOCS: 'service-doc'
};

/*
 Loading the Index resource.
 */
const api = fetch('/api')
    .then(response => response.json())
    .then(data => data['_links']);

/*
 Resolve an API resource through a link relation and any parameters.
 */
async function call(relation, params) {
    const relations = await api;
    const link = relations[relation];
    if (!link) {
        throw new Error(`Unknown resource or operation: ${relation}`)
    }

    const uri = link.templated ?
        parseTemplate(link.href).expand(params) : link.href;
    const response = await fetch(uri);

    return link.type && link.type.includes('json') ?
        response.json() : response.text();
}

/*
 Resolves the current date and time.
 */
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
 * Converts a date. Required format "yyyy-mm-dd"
 */
async function convertDate(dateString) {
    const [year, month, day] = dateString.split('-');
    const data = await call(rel.DATE, {year, month, day});
    return parseDate(data);
}

/*
 * Converts a timestamp. Required format "hh:mm:ss"
 */
async function convertTime(timeString) {
    const [hour, minute, second] = timeString.split(':');
    const data = await call(rel.TIME, {hour, minute, second});
    return parseTime(data);
}

/*
 Flattens and simplifies a Date JSON resource into a Javascript object.
 */
function parseDate(api_date) {
    const wikiLinks = api_date['_links'][rel.WIKI];

    const dayLink = wikiLinks.find(l => l.name === 'day').href;
    const monthLink = wikiLinks.find(l => l.name === 'month').href;

    return {
        date: api_date.texts.default,
        dateShort: api_date.texts.short,
        observance: api_date.texts.observance.tagged,

        yearRoman: api_date.attributes.year.roman,
        yearArabic: api_date.attributes.year.arabic,

        monthName: api_date.attributes.month.name,
        monthNumber: api_date.attributes.month.number,

        dayNumberMonth: api_date.attributes.day.number_in_month,
        dayName: api_date.attributes.day.name,

        observingMonth: api_date.attributes.month.entity.name,
        observingDay: api_date.attributes.day.entity.name,

        dayLink,
        monthLink
    }
}

/*
 Flattens and simplifies a Time JSON resource into a Javascript object.
 */
function parseTime(api_time) {
    return {
        timeString: api_time.texts.default,
        timeDecimal: api_time.texts.decimal,
        hour: api_time.attributes.hour,
        minute: api_time.attributes.minute,
        second: api_time.attributes.second
    };
}

/*
 Get the XSL Transform stylesheet for turning the tagged observance text into HTML.
 */
async function getObservanceTransform() {
    return call(rel.TRANSFORM, null);
}

/*
 Get API documentation in Markdown.
 */
async function getDocs() {
    return call(rel.DOCS, null);
}

export {
    getNow,
    convertDate,
    convertTime,
    getObservanceTransform,
    getDocs
}