const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const merge = require('webpack-merge');
const devserver = require('./webpack/devserver');
const pug = require('./webpack/pug');
const sass = require('./webpack/sass');
const extractCSS = require('./webpack/extract.css');
const files = require('./webpack/files');

module.exports = merge ([
    {
        mode: 'development',
        context: __dirname,
        entry: {
            main: [
                './assets/js/index',
                'jquery',
            ]
        },
        output: {
            path: path.resolve('./hotel/static'),
            filename: "./js/[name].js"
        },
        plugins: [
            new HtmlWebpackPlugin({
                template: 'hotel/templates/pug/index.pug',
            }),
            new BundleTracker({
                filename: './webpack-stats.json',
            }),
            new CopyWebpackPlugin([
                { from: 'assets/images', to: 'vendors/images' },
                { from: 'assets/fonts', to: 'vendors/fonts' },
                { from: 'assets/jquery', to: 'vendors/jquery' },
            ]),
            new webpack.ProvidePlugin({
                $: "jquery",
                jQuery: "jquery",
                jquery: "jquery"
            })
        ]
    },
    devserver(),
    pug(),
    sass(),
    extractCSS(),
    files()
]);