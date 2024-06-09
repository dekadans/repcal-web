const path = require('path');

module.exports = {
    entry: './js/index.js',
    output: {
        filename: 'dist.js',
        path: path.resolve(__dirname, 'static'),
    },
    mode: "development"
};