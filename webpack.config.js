const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  mode: 'development', // maini uz 'production' kad būvē
  entry: './static/js/index.js',
  output: {
    path: path.resolve(__dirname, 'static/dist/'),
    filename: '[name].[contenthash].js',
    publicPath: '/static/dist/',
    clean: true,
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
        test: /\.m?js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
  resolve: {
    fullySpecified: false,
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
    }),
    new BundleTracker({
      path: __dirname,
      filename: 'webpack-stats.json',
    })

  ],
};
