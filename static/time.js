let app = new Vue({
    el: '#app',
    data: {
        hour: 0,
        minute: 0,
        second: 0,
        date: '',
        offset: 0,
        interval: null
    },
    template: /*html*/`
        <div>
            <h1>{{ date }}</h1>
            <h2>{{ hour }}:{{ minute }}:{{ second }}</h2>
        </div>
    `,
    created: function() {
        this.offset = (new Date()).getTimezoneOffset() * -1;
        this.sync();
        this.interval = setInterval(this.tick, 864);

        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.sync();
            }
        });
    },
    methods: {
        sync: function() {
            fetch('/now?offset=' + this.offset)
            .then(response => response.json())
            .then(data => {
                const rep_time = data._embedded['repcal:time'];
                const rep_date = data._embedded['repcal:date'];
                this.hour = rep_time.attributes.hour;
                this.minute = rep_time.attributes.minute;
                this.second = rep_time.attributes.second;
                this.date = rep_date.texts.default;
            });
        },
        tick: function() {
            this.second++;

            if (this.second === 100) {
                this.second = 0;
                this.minute++;

                if (this.minute === 100) {
                    this.minute = 0;
                    this.hour++;

                    if (this.hour === 10) {
                        this.hour = 0;
                        this.sync();
                    }
                }
            }
        }
    }
});