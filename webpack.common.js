const path = require("path");
const ManifestPlugin = require("webpack-manifest-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const DotenvPlugin = require("dotenv-webpack");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const targetPath = path.resolve(__dirname, "app/assets/dist");
module.exports.targetPath = targetPath;

module.exports = {
  entry: {
    "layouts/base": "./app/js/pages/layouts/base.ts",
    "base/index": "./app/js/pages/base/index.ts",
    "raffles/index": "./app/js/pages/raffles/index.js",
    "raffles/new": "./app/js/pages/raffles/new.js",
    "raffles/status": "./app/js/pages/raffles/status.js",
    "raffles/show": "./app/js/pages/raffles/show.js",
    "users/show": "./app/js/pages/users/show.js",
  },
  output: {
    filename: "[name].[contenthash].js",
    path: targetPath,
  },
  resolve: {
    alias: {
      "@js": path.resolve(__dirname, "app/js"),
      "@assets": path.resolve(__dirname, "app/assets"),
    },
    extensions: [".ts", ".tsx", ".js", ".jsx", ".css", ".scss"],
    modules: ["node_modules", "app/assets/css"],
  },
  plugins: [
    new DotenvPlugin({ systemvars: true }),
    new CleanWebpackPlugin({ verbose: true, dry: false }),
    new ManifestPlugin({
      generate: (seed, files, entrypoints) => {
        // https://github.com/danethurber/webpack-manifest-plugin/issues/181
        // Generates a manifest in the format of { [entrypoint: string]: Array<string> }
        return entrypoints;
      },
    }),
    new MiniCssExtractPlugin({
      filename: "[name].[contenthash].css",
    }),
  ],
  module: {
    rules: [
      {
        enforce: "pre",
        test: /\.(sc|sa|c)ss$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        enforce: "pre",
        test: /\.(t|j)s(x?)$/,
        exclude: /node_modules/,
        loader: "eslint-loader",
      },
      {
        test: /\.(t|j)s(x?)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            configFile: true,
          },
        },
      },
    ],
  },
  optimization: {
    splitChunks: {
      chunks: "all",
    },
  },
};
