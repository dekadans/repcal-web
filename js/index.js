import Alpine from 'alpinejs'
import now from './now'
import * as details from './details'

function initNow() {
    document.addEventListener('alpine:init', () => {
        Alpine.data('now', now);
    });
    Alpine.start();
}

function initDetails() {
    document.addEventListener('alpine:init', () => {
        Alpine.data('dateDetails', details.date);
        Alpine.data('timeDetails', details.time);
    });
    Alpine.start();
}

window.repcal = {
    initNow,
    initDetails
}