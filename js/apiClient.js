import {parseTemplate} from "url-template";

/*
 Link relations for defined operations and resources.
 */
const rel = {
    NOW: 'repcal:now',
    DATE: 'repcal:date',
    TIME: 'repcal:time',
    OBSERVANCE: 'repcal:observance',
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

    return resolveLink(link, params);
}

/*
 Resolves a resource from a HAL link object.
 */
async function resolveLink(link, params) {
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
    const apiResponse = await call(rel.NOW, {offset});

    const date = apiResponse['_embedded'][rel.DATE];
    const time = apiResponse['_embedded'][rel.TIME];
    const observance = date['_embedded'][rel.OBSERVANCE];

    return {
        ...parseDate(date, observance),
        ...parseTime(time)
    };
}

/*
 * Converts a date. Required format "yyyy-mm-dd"
 */
async function convertDate(dateString) {
    const [year, month, day] = dateString.split('-');
    const apiDate = await call(rel.DATE, {year, month, day});

    const observanceLink = apiDate['_links'][rel.OBSERVANCE];
    const apiObservance = await resolveLink(observanceLink, null);

    return parseDate(apiDate, apiObservance);
}

/*
 * Converts a timestamp. Required format "hh:mm:ss"
 */
async function convertTime(timeString) {
    const [hour, minute, second] = timeString.split(':');
    const apiTime = await call(rel.TIME, {hour, minute, second});
    return parseTime(apiTime);
}

/*
 Flattens and simplifies Date and Observance JSON resources into a Javascript object.
 */
function parseDate(apiDate, apiObservance) {
    const wikiLinks = apiObservance['_links'][rel.WIKI];

    return {
        date: apiDate.texts.default,
        dateShort: apiDate.texts.short,

        yearRoman: apiDate.attributes.year.roman,
        yearArabic: apiDate.attributes.year.arabic,

        monthName: apiDate.attributes.month.name,
        monthNumber: apiDate.attributes.month.number,

        dayNumberMonth: apiDate.attributes.day.number_in_month,
        dayName: apiDate.attributes.day.name,

        observance: apiObservance.texts.tagged,
        observingMonth: apiObservance.attributes.month.name,
        observingDay: apiObservance.attributes.day.name,

        dayLink: wikiLinks.find(l => l.name === 'day').href,
        monthLink: wikiLinks.find(l => l.name === 'month').href
    }
}

/*
 Flattens and simplifies a Time JSON resource into a Javascript object.
 */
function parseTime(apiTime) {
    return {
        timeString: apiTime.texts.default,
        timeDecimal: apiTime.texts.decimal,
        hour: apiTime.attributes.hour,
        minute: apiTime.attributes.minute,
        second: apiTime.attributes.second
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