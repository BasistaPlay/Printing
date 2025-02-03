const path = require('path');

module.exports = {
  mode: 'development', // Pievieno šo rindiņu
  entry: './static/js/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/dist'),
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'static'),
    },
    compress: true,
    port: 9000,
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
};
