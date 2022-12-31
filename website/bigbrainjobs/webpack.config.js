const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const ImageMinimizerPlugin = require("image-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  mode: 'production',
  entry: './static/src/main.js',
  target: 'web',
  output: {
    path: path.resolve(__dirname, 'static/dist'),
    clean: true,
    assetModuleFilename: 'images/[name][ext][query]',
  },
  plugins: [
    new MiniCssExtractPlugin(),
    // new BundleAnalyzerPlugin()
  ],
  module: {
    rules: [
      {
        test: /\.scss$/i,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  [
                    "autoprefixer",
                    {
                      // Options
                    },
                  ],
                ],
              }
            }
          },
          {
            loader: 'sass-loader',
          }
        ]
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
      {
        test: /favicon.png$/i,
        type: 'asset/resource',
        generator: {
          filename: '[name][ext][query]',
        }
      },
    ]
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          format: {
            comments: false,
          },
        },
        extractComments: false,
      }),
      new CssMinimizerPlugin({
        minimizerOptions: {
          preset: [
            'default',
            {
              discardComments: { removeAll: true },
            },
          ],
        },
      }),
      new ImageMinimizerPlugin({
        // minimizer: {
        //   implementation: ImageMinimizerPlugin.sharpMinify,
        //   options: {
        //     encodeOptions: {
        //       png: {
        //         compressionLevel: 9,
        //         quality: 1,
        //       },
        //       jpeg: {
        //         quality: 90,
        //       },
        //     },
        //   },
        // },
        generator: [
          {
            preset: 'favicon',
            implementation: ImageMinimizerPlugin.sharpGenerate,
            options: {
              resize: {
                width: 32,
              },
              encodeOptions: {
                png: {
                  compressionLevel: 9,
                  quality: 1,
                },
              },
            },
          },
          {
            preset: 'webp',
            implementation: ImageMinimizerPlugin.sharpGenerate,
            options: {
              resize: {
              },
              encodeOptions: {
                webp: {
                },
              },
            },
          },
        ],
      }),
    ],
  },
};
