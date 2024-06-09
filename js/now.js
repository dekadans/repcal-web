import * as apiClient from "./apiClient";

export default () => ({
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
        Object.assign(this, await apiClient.getNow());
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