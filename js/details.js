import * as apiClient from "./apiClient";

export default () => ({
    input: '',

    init() {
        const now = new Date();
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const date = now.getDate().toString().padStart(2, '0');
        this.input = `${now.getFullYear()}-${month}-${date}`;
    },

    convert() {
        apiClient.convertDate(this.input);
    }
});