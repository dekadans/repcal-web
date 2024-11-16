import * as apiClient from "./apiClient.js"
import {marked} from "marked";

export default () => ({
    text: '',

    async init() {
        this.text = marked.parse(
            await apiClient.getDocs()
        );
    }
});