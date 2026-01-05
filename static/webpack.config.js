const path = require('path');

module.exports = {
  entry: './src/index.js', // Your main ES6 entry file
  output: {
    filename: 'bundle.js', // The output ES5 bundle
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
};
