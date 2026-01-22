const path = require('path');

/**
 * Configs for front-end CRM + PM UI/UX
 * Future node.js configurations should be defined in a seperate variable
 */
const appConfig = {
    mode: 'development', // on prod change to: 'production',
    entry: {
        // Defines two separate entry points and their output names
        'users-bundle': path.resolve(__dirname, './users/js/main.js'),
        'tasks-bundle': path.resolve(__dirname, './tasks/js/main.js')
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
    resolve: {
        fallback: {
        "path": require.resolve("path-browserify")
        }
    },
};

// Export a function so we can select a single entry with `--env entry=core|tasks`
module.exports = (env = {}) => {
    const entry = env.entry;

    if (entry === 'users') {
        return {
            mode: 'development',
            entry: path.resolve(__dirname, './users/js/main.js'),
            output: {
                filename: 'users-bundle.js',
                path: path.resolve(__dirname, 'dist'),
            },
            module: appConfig.module,
            stats: appConfig.stats,
            resolve: {
                fallback: {
                "path": require.resolve("path-browserify")
                }
            },
        };
    }

    if (entry === 'tasks') {
        return {
            mode: 'development',
            entry: path.resolve(__dirname, './tasks/js/main.js'),
            output: {
                filename: 'tasks-bundle.js',
                path: path.resolve(__dirname, 'dist'),
            },
            module: appConfig.module,
            stats: appConfig.stats,
            resolve: {
                fallback: {
                "path": require.resolve("path-browserify")
                }
            },
        };
    }

    // Default: build both bundles
    return appConfig;
};