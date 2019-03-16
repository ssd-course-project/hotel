const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = function () {
    return {
        module: {
            rules: [
                {
                    test: /\.s?css$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        "css-loader",
                        "sass-loader"
                    ]
                }
            ]
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: "./css/[name].css",
                chunkFilename: "./css/[id].css"
            })
        ]
    }
};