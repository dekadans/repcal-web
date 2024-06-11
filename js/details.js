import * as apiClient from "./apiClient";

const date = () => ({
    input: '',
    data: false,

    init() {
        const now = new Date();
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const date = now.getDate().toString().padStart(2, '0');
        this.input = `${now.getFullYear()}-${month}-${date}`;
    },

    async convert() {
        this.data = await apiClient.convertDate(this.input);
    }
});

const time = () => ({
    input: '',

    init() {
        const now = new Date();
        const hour = now.getHours().toString().padStart(2, '0');
        const minute = now.getMinutes().toString().padStart(2, '0');
        const second = now.getSeconds().toString().padStart(2, '0');
        this.input = `${hour}:${minute}:${second}`;
    },

    convert() {
        apiClient.convertTime(this.input);
    }
})

export {
    date,
    time
}