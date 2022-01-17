const path = require('path');
const webpack = require('webpack');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const autoprefixer = require('autoprefixer');


process.traceDeprecation = true;

module.exports = (env, options) =>
{
    const isDevelopment = options.mode !== 'production';
    return {
        entry: {
            main: [path.resolve(__dirname, 'website/sass/app.scss')],
        },
        output: {
            path: path.resolve(__dirname, 'static'),
            publicPath: '/assets/',
            filename: 'css/[name].js',
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: 'css/[name].css',
            }),
            new WebpackManifestPlugin({
                fileName: path.resolve(__dirname,
                    '../var/web/webpack-css.meta.json'),
                filter: (f) =>
                    {
                        return f.name.endsWith('.css');
                    },
                sort: (a, b) =>
                    {
                        let splita = a.name.split('~');
                        let splitb = b.name.split('~');
                        return splitb.length - splita.length;
                    },
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.s[ac]ss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: {
                                sourceMap: isDevelopment,
                                url: false,
                            },
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                postcssOptions: { plugins: [autoprefixer()] },
                            },
                        },
                        'resolve-url-loader',
                        {
                            loader: 'sass-loader',
                            options: {
                                implementation: require('sass'),
                                sourceMap: isDevelopment,
                                // See https://github.com/webpack-contrib/sass-loader/issues/804
                                webpackImporter: false,
                                sassOptions: {
                                    includePaths: [
                                        path.resolve(__dirname,
                                            '../node_modules'),
                                    ],
                                },
                            },
                        },
                    ],
                },
                {
                    test: /\.css$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        {
                            loader: 'css-loader',
                            options: { sourceMap: isDevelopment },
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                postcssOptions: { plugins: [autoprefixer()] },
                            },
                        },
                        'resolve-url-loader',
                    ],
                },
            ],
        },
        optimization: {
            runtimeChunk: 'single',
            splitChunks: {
                chunks: 'all',
                cacheGroups: {
                    base: {
                        name: 'base',
                        test: /[\\/]node_modules[\\/](@material)[\\/]/,
                        enforce: true,
                    },
                },
            },
            minimizer: [
                '...',
                new CssMinimizerPlugin(),
            ],
        },
        devtool: isDevelopment ? 'source-map' : false,
    };
};
