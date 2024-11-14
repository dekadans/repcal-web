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
 HAL-related reserved keys.
 */
const hal = {
    LINKS: '_links',
    EMBED: '_embedded'
}

/*
 Loading the Index resource.
 */
const api = fetch('/api')
    .then(response => response.json())
    .then(data => data[hal.LINKS]);

/*
 Finds a link from the API Index based on relation (and name, for to-many relationships.)
 */
async function index(relation, name) {
    const relations = await api;
    let link = relations[relation];
    if (Array.isArray(link)) {
        link = link.find(_ => _.name === name);
    }

    return link;
}

/*
 Resolves a resource from a HAL link object.
 */
async function resolve(link, params) {
    const uri = link.templated ?
        parseTemplate(link.href).expand(params) : link.href;
    const response = await fetch(uri);

    if (!response.ok) {
        alert('The request could not be fulfilled.');
        throw new Error(`An API request got response code ${response.status}.`);
    }

    return link.type && link.type.includes('json') ?
        response.json() : response.text();
}

/*
 Resolves the current date and time.
 */
function getNow() {
    const offset = (new Date()).getTimezoneOffset() * -1;

    return index(rel.NOW)
        .then(l => resolve(l, {offset}))
        .then(apiResponse => {
            const date = apiResponse[hal.EMBED][rel.DATE];
            const time = apiResponse[hal.EMBED][rel.TIME];
            const observance = date[hal.EMBED][rel.OBSERVANCE];

            return {
                ...parseDate(date, observance),
                ...parseTime(time)
            };
        });
}

/*
 * Converts a date. Required format "yyyy-mm-dd"
 */
function convertDate(dateString) {
    try {
        const [year, month, day] = handleInput(dateString, '-');

        return index(rel.DATE)
            .then(l => resolve(l, {year, month, day}))
            .then(apiDate => {
                return Promise.all([
                    apiDate,
                    resolve(apiDate[hal.LINKS][rel.OBSERVANCE])
                ]);
            })
            .then(data => parseDate(...data))
    } catch (e) {
        alert('Invalid input date.');
        return false;
    }
}

/*
 * Converts a timestamp. Required format "hh:mm:ss"
 */
function convertTime(timeString) {
    try {
        const [hour, minute, second] = handleInput(timeString, ':');

        return index(rel.TIME)
            .then(l => resolve(l, {hour, minute, second}))
            .then(t => parseTime(t));
    } catch (e) {
        alert('Invalid input time.');
        return false;
    }
}

/*
 Splits and validates input.
 */
function handleInput(value, separator) {
    const parts = value.split(separator);
    if (parts.length < 3) {
        throw Error('Invalid input');
    }
    return parts;
}

/*
 Flattens and simplifies Date and Observance JSON resources into a Javascript object.
 */
function parseDate(apiDate, apiObservance) {
    const wikiLinks = apiObservance[hal.LINKS][rel.WIKI];

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

        dayLink: wikiLinks.find(_ => _.name === 'day').href,
        monthLink: wikiLinks.find(_ => _.name === 'month').href
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
function getObservanceTransform() {
    return index(rel.TRANSFORM, 'observance').then(_ => resolve(_));
}

/*
 Get API documentation in Markdown.
 */
function getDocs() {
    return index(rel.DOCS).then(_ => resolve(_));
}

export {
    getNow,
    convertDate,
    convertTime,
    getObservanceTransform,
    getDocs
}