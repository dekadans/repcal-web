async function getData() {
    const offset = (new Date()).getTimezoneOffset() * -1;
    const response = await fetch('/now?offset=' + offset);
    const data = await response.json();

    return {
        ...parseDate(data._embedded['repcal:date']),
        ...parseTime(data._embedded['repcal:time'])
    };
}

function parseDate(api_date) {
    const links = api_date._links['repcal:meta-day'];
    const uiLink = links.find(l => l.name === 'ui');

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

const nowApp = () => ({
    date: 'Loading...',
    hour: 0,
    minute: 0,
    second: 0,
    celebrating: '...',
    wiki: '#',

    init() {
        this.sync();

        setInterval(() => {
            this.tick();
        }, 864);

        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.sync();
            }
        });
    },

    async sync() {
        Object.assign(this, await getData());
    },

    tick() {
        this.second = (this.second + 1) % 100;

        if (this.second === 0) {
            this.minute = (this.minute + 1) % 100;

            if (this.minute === 0) {
                this.hour = (this.hour + 1) % 10;

                if (this.hour === 0) {
                    this.sync();
                }
            }
        }
    }
});