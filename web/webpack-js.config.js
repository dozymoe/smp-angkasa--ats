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
            main: [path.resolve(__dirname, 'website/js/app.js')],
        },
        output: {
            path: path.resolve(__dirname, '../public/web'),
            publicPath: '/',
            filename: 'assets/js/[name].js',
        },
        resolve: {
            alias: {
            },
        },
        plugins: [
            new LodashModuleReplacementPlugin(),
            new webpack.IgnorePlugin(/^\.\/locale$/),
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
                        const order = ['runtime.js', 'polyfill', 'base', 'react'];
                        let splita = a.name.split('~');
                        let splitb = b.name.split('~');
                        let indexa = order.indexOf(splita[0]);
                        let indexb = order.indexOf(splitb[0]);
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
                        if (splitb.length - splita.length)
                        {
                            return splitb.length - splita.length;
                        }
                        return b.name.length - a.name.length;
                    },
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.css$/,
                    use: ['null-loader'],
                },
                {
                    test: /\.svg$/,
                    use: [
                        {
                            loader: 'html-loader',
                            options: {
                                minimize: true,
                            },
                        },
                    ],
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
                                        '@babel/plugin-transform-regenerator',
                                        {generators: true},
                                    ],
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
                                    '@babel/preset-react',
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
                        test: /[\\/]node_modules[\\/](@material|lodash)[\\/]/,
                    },
                    polyfill: {
                        name: 'polyfill',
                        test: /[\\/]node_modules[\\/](core-js|regenerator-runtime|element-closest-polyfill)[\\/]/,
                    },
                    react: {
                        name: 'react',
                        test: /[\\/]node_modules[\\/](mobx|mobx-react|react|react-dom|react-router|react-router-dom|preact|preact-compat)[\\/]/,
                    },
                },
            },
        },
        devtool: isDevelopment ? 'source-map' : false,
    };
};
