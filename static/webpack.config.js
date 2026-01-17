const path = require('path');

/**
 * Configs for front-end CRM + PM UI/UX
 * Future node.js configurations should be defined in a seperate variable
 */
const appConfig = {
    mode: 'development', // on prod change to: 'production',
    entry: {
        // Defines two separate entry points and their output names
        'core-bundle': path.resolve(__dirname, './core/js/custom.js'),
        'tasks-bundle': path.resolve(__dirname, './tasks/js/custom.js')
    },
    output: {
        filename: '[name].js', // The output ES5 bundle, [name] is replaced by the entry key
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
        errorDetails: true,
    },
};

// Export a function so we can select a single entry with `--env entry=core|tasks`
module.exports = (env = {}) => {
    const entry = env.entry;

    if (entry === 'core') {
        return {
            mode: 'development',
            entry: path.resolve(__dirname, './core/js/custom.js'),
            output: {
                filename: 'core-bundle.js',
                path: path.resolve(__dirname, 'dist'),
            },
            module: appConfig.module,
            stats: appConfig.stats,
        };
    }

    if (entry === 'tasks') {
        return {
            mode: 'development',
            entry: path.resolve(__dirname, './tasks/js/custom.js'),
            output: {
                filename: 'tasks-bundle.js',
                path: path.resolve(__dirname, 'dist'),
            },
            module: appConfig.module,
            stats: appConfig.stats,
        };
    }

    // Default: build both bundles
    return appConfig;
};