const path = require('path');

/**
 * Configs for front-end CRM + PM UI/UX
 * Future node.js configurations should be defined in a seperate variable
 */
const dummy = {
    mode: 'development', // on prod change to: 'production',
    entry: path.resolve(__dirname, './src/index.js'),
    output: {
        filename: 'bundle.js', // The output ES5 bundle, [name] is replaced by the entry key
        path: path.resolve(__dirname, 'dist'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
        ],
    },
    stats: {
        errorsDetails: true,
    },
};

const coreConfig = {
    mode: 'development', // on prod change to: 'production',
    entry: path.resolve(__dirname, './core/js/custom.js'),
    output: {
        filename: 'core.js', // The output ES5 bundle, [name] is replaced by the entry key
        path: path.resolve(__dirname, 'dist'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
        ],
    },
    stats: {
        errorsDetails: true,
    },
};

const appConfig = {
    mode: 'development', // on prod change to: 'production',
    entry: {
        // Defines two separate entry points and their output names
        'dist/core-bundle': './src/core.js',
        'dist/tasks-bundle': './src/tasks.js'
    },
    output: {
        filename: '[name].js', // The output ES5 bundle, [name] is replaced by the entry key
        path: path.resolve(process.cwd(), './'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                },
            },
        ],
    },
    stats: {
        errorsDetails: true,
    },
};

module.exports[appConfig];