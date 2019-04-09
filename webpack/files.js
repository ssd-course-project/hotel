module.exports = function() {
    return {
        module: {
            rules: [
                {
                    test: /\.(jpg|png|svg|ttf|eot|woff|woff2)$/,
                    loader: 'file-loader',
                    options: {
                        name: '[path][name].[ext]'
                    },
                },
            ],
        },
    };
};