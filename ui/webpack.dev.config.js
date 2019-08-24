const merge = require('webpack-merge');
const common = require('./webpack.config.js');

module.exports = merge(common, {
    mode: "development",

    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",

    performance: {
        hints: false
    },

    devServer: {
        contentBase: [__dirname + '/dist', __dirname + '/../runtime', __dirname],
        port: 7709
    }
})
