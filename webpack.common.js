const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

const targetPath = path.resolve(__dirname, "app/assets/js_build");
module.exports.targetPath = targetPath;

module.exports = {
  entry: {
    main: "./app/js/index.js",
    "layouts/footer": "./app/js/pages/layouts/footer.js",
    "layouts/header": "./app/js/pages/layouts/header.js",
  },
  output: {
    filename: "[name].[contenthash].js",
    path: targetPath,
  },
  plugins: [
    new CleanWebpackPlugin({ verbose: true, dry: false }),
    new ManifestPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
};
