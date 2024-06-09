import Alpine from 'alpinejs'
import now from './now'
import dateDetails from './details'

function initNow() {
    document.addEventListener('alpine:init', () => {
        Alpine.data('now', now);
    });
    Alpine.start();
}

function initDetails() {
    document.addEventListener('alpine:init', () => {
        Alpine.data('dateDetails', dateDetails);
    });
    Alpine.start();
}

window.repcal = {
    initNow,
    initDetails
}