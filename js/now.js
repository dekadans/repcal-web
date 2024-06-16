import * as apiClient from "./apiClient";

export default () => ({
    hour: 0,
    minute: 0,
    second: 0,

    date: 'Loading...',
    dateShort: '',
    observance: '',
    dayLink: '#',
    monthLink: '#',

    transformXml: null,

    init() {
        this.transformXml = apiClient.getObservanceTransform();
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
        const [
            now,
            stylesheet
        ] = await Promise.all([apiClient.getNow(), this.transformXml]);

        now.observance = this.transformObservance(
            now.observance,
            stylesheet,
            {day: now.dayLink, month: now.monthLink}
        );

        Object.assign(this, now);
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
    },

    transformObservance(input, stylesheet, links) {
        const xml = new DOMParser().parseFromString(input, 'application/xml');
        const xslt = new DOMParser().parseFromString(stylesheet, 'application/xml');

        const xsltProcessor = new XSLTProcessor();
        xsltProcessor.importStylesheet(xslt);
        xsltProcessor.setParameter(null, 'dayUrl', links.day);
        xsltProcessor.setParameter(null, 'monthUrl', links.month);

        return new XMLSerializer().serializeToString(
            xsltProcessor.transformToFragment(xml, document)
        );
    }
});