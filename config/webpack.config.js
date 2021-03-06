var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
  context: path.join(__dirname, '../app/assets/javascripts'),
  entry: {
    vendor: './vendor.js',
    common: './common.js',
    app: './main.js'
  },
  output: {
    path: path.join(__dirname, '../static/javascripts'),
    filename: '[name].js'
  },
  resolve: {
    extensions: ['.js', '.coffee']
  },
  module: {
    // FIXME: add babel-loader
    rules: [
      {
        test: require.resolve('jquery'),
        use: [{
          loader: 'expose-loader',
          options: 'jQuery'
        },{
          loader: 'expose-loader',
          options: '$'
        }]
      }, {
        test: require.resolve('tether'),
        use: [{
          loader: 'expose-loader',
          options: 'Tether'
        }]
      }, {
        test: require.resolve('popper.js'),
        use: [{
          loader: 'expose-loader',
          options: 'Popper'
        }]
      }, {
        test: /\.coffee$/,
        use: 'coffee-loader'
      }, {
        test: /\.(sass|scss)?$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          //resolve-url-loader may be chained before sass-loader if necessary
          use: [{
            loader: 'css-loader'
          }, {
            loader: 'postcss-loader',
            options: {
              plugins: function () { // post css plugins, can be exported to postcss.config.js
                return [
                  require('precss'),
                  require('autoprefixer')
                ];
              }
            }
          }, {
            loader: 'sass-loader'
          }]
        })
      }, {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }, {
        test: /\.font\.js/,
        loader: ExtractTextPlugin.extract({
          use: [
            'css-loader',
            'webfonts-loader'
          ]
        })
      }
    ]
  },
  /**
   * FIXME: refactor webpack config
   * Add configuration for development environment and production environment
   * respectively. In production environment, the css and js files are 
   * required to be compressed.
   */
  plugins: [
    new ExtractTextPlugin('../stylesheets/[name].css')
  ]
};
