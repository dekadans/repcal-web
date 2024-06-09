import {parseTemplate} from "url-template";

const rel = {
    NOW: 'repcal:now',
    DATE: 'repcal:date',
    TIME: 'repcal:time'
};

const api = (async () => {
    return fetch('/api')
        .then(response => response.json())
        .then(data => data._links);
})();

async function call(rel, params) {
    const relations = await api;
    const uri = parseTemplate(relations[rel].href).expand(params);
    const response = await fetch(uri);
    return await response.json();
}

async function getNow() {
    const offset = (new Date()).getTimezoneOffset() * -1;
    const data = await call(rel.NOW, {offset});

    return {
        ...parseDate(data._embedded[rel.DATE]),
        ...parseTime(data._embedded[rel.TIME])
    };
}

async function convertDate(dateString) {
    const [year, month, day] = dateString.split('-');
    const data = await call(rel.DATE, {year, month, day});
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