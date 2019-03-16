const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const merge = require('webpack-merge');
const devserver = require('./webpack/devserver');
const pug = require('./webpack/pug');
const sass = require('./webpack/sass');
const extractCSS = require('./webpack/extract.css');

module.exports = merge ([
    {
        mode: 'development',
        context: __dirname,
        entry: './assets/js/index',
        output: {
            path: path.resolve('./hotel/static'),
            filename: "./js/[name].js"
        },
        plugins: [
            new BundleTracker({
                filename: './webpack-stats.json',
            }),
            new MiniCssExtractPlugin({
                filename: "./css/[name].css",
                chunkFilename: "./css/[id].css"
            })
        ]
    },
    devserver(),
    pug(),
    sass(),
    extractCSS(),
]);