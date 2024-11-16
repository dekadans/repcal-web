import Alpine from 'alpinejs'
import now from './now.js'
import * as details from './details.js'
import docs from './docs.js'

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

function initDocs() {
    document.addEventListener('alpine:init', () => {
        Alpine.data('docs', docs);
    });
    Alpine.start();
}

window.repcal = {
    initNow,
    initDetails,
    initDocs
}