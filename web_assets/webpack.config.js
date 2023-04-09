const path = require('path');
const webpack = require('webpack');
const LodashModuleReplacementPlugin = require('lodash-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

process.traceDeprecation = true;

module.exports = (env, options) =>
{
    const isDevelopment = options.mode !== 'production';
    return {
        entry: {
            main: [path.resolve(__dirname, 'main.js')],
        },
        output: {
            path: path.resolve(__dirname, '../web/static/js'),
            publicPath: '/assets/js/',
            filename: '[chunkhash].js',
        },
        resolve: {
            alias: {
            },
        },
        plugins: [
            new webpack.DefinePlugin({
                __DEV__: isDevelopment,
            }),
            new LodashModuleReplacementPlugin(),
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
                'window.jQuery': 'jquery',
            }),
            new WebpackManifestPlugin({
                fileName: path.resolve(__dirname,
                    '../var/web/webpack-js.meta.json'),
                sort: (a, b) =>
                    {
                        const order = ['runtime', 'polyfill', 'base', 'fw'];
                        let namea = a.name.split('.')[0];
                        let nameb = b.name.split('.')[0];
                        let indexa = order.indexOf(namea);
                        let indexb = order.indexOf(nameb);
                        if (indexa !== -1 && indexb !== -1)
                        {
                            return indexa - indexb;
                        }
                        else if (indexa !== -1)
                        {
                            return -1;
                        }
                        else if (indexb !== -1)
                        {
                            return 1;
                        }
                        return nameb.length - namea.length;
                    },
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.css$/,
                    loader: 'null-loader',
                },
                {
                    test: /\.svg$/,
                    loader: 'html-loader',
                    options: {minimize: true},
                },
                {
                    test: /\.html$/,
                    loader: 'raw-loader',
                },
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader',
                            options: {
                                presets: [
                                    [
                                        '@babel/preset-env',
                                        {
                                            modules: false,
                                            useBuiltIns: 'usage',
                                            corejs: {
                                                version: 3,
                                                proposals: true,
                                            },
                                        },
                                    ],
                                ],
                                plugins: [
                                    [
                                        '@babel/plugin-proposal-decorators',
                                        {legacy: true},
                                    ],
                                    [
                                        '@babel/plugin-proposal-class-properties',
                                        {loose: true},
                                    ],
                                    [
                                        '@babel/plugin-proposal-private-methods',
                                        {loose: true},
                                    ],
                                    [
                                        '@babel/plugin-proposal-private-property-in-object',
                                        {loose: true},
                                    ],
                                    [
                                        '@babel/plugin-transform-regenerator',
                                        {generators: true},
                                    ],
                                    [
                                        '@babel/plugin-transform-react-jsx',
                                        {pragma: 'm', pragmaFrag: "'['"},
                                    ],
                                    '@babel/plugin-syntax-dynamic-import',
                                    'lodash',
                                ],
                            },
                        },
                    ],
                },
                {
                    test: /\.jsx$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'babel-loader',
                            options: {
                                presets: [
                                    [
                                        '@babel/preset-env',
                                        {
                                            modules: false,
                                            useBuiltIns: 'usage',
                                            corejs: {
                                                version: 3,
                                                proposals: true,
                                            },
                                        },
                                    ],
                                ],
                                plugins: [
                                    [
                                        '@babel/plugin-proposal-decorators',
                                        {legacy: true},
                                    ],
                                    [
                                        '@babel/plugin-proposal-class-properties',
                                        {loose: true},
                                    ],
                                    [
                                        '@babel/plugin-proposal-private-methods',
                                        {loose: true},
                                    ],
                                    [
                                        '@babel/plugin-proposal-private-property-in-object',
                                        {loose: true},
                                    ],
                                    [
                                        '@babel/plugin-transform-regenerator',
                                        {generators: true},
                                    ],
                                    'lodash',
                                ],
                            },
                        },
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
                        test: /[\\/]node_modules[\\/](@carbon|carbon-components|lodash|jquery)[\\/]/,
                    },
                    polyfill: {
                        name: 'polyfill',
                        test: /[\\/]node_modules[\\/](core-js|regenerator-runtime|element-closest-polyfill|flatpickr)[\\/]/,
                    },
                    fw: {
                        name: 'fw',
                        test: /[\\/]node_modules[\\/](unistore|mithril|mithril-node-render)[\\/]/,
                    },
                },
            },
        },
        devtool: isDevelopment ? 'source-map' : false,
    };
};
