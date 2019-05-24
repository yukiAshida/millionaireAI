1. 初期処理
```
npm init -y
```

2. package.jsonの変更
```json
{
    "name": "hello_react",
    "version": "1.0.0",
    "description": "Hello React",
    "private": true,
    "main": "index.js",
    "scripts": {
        "start": "webpack-dev-server",
        "build": "webpack -d"
    },
　　"keywords": [],
　　"author": "",
　　"license": "ISC"
}
```

3. 種々のパッケージのインスト―ル
```
npm install react react-dom
npm install webpack webpack-cli webpack-dev-server --save-dev
npm install @babel/core @babel/preset-env @babel/preset-react --save-dev
npm install eslint babel-eslint eslint-loader eslint-plugin-react --save-dev
npm install css-loader style-loader babel-loader --save-dev

npm install --save-dev file-loader url-loader   // 画像の読み込みのため
npm install --savee-dev superagent   // flaskとのajax処理のため
```

4. ディレクトリと設定ファイルの生成

* srcフォルダ
* publicフォルダ

* .babelr
```json
{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}
```

* .eslintrc.json
```json
{
 "parser": "babel-eslint",
  "env": {
    "browser": true,
    "es6": true
  },
  "parserOptions": {
    "sourceType": "module",
    "ecmaFeatures": {
      "experimentalObjectRestSpread": true,
      "jsx": true
    }
  },
  "extends": ["eslint:recommended", "plugin:react/recommended"],
  "plugins": ["react"],
  "rules": {
    "no-console": "off",
    "react/prop-types":"off", /*好み*/
    "no-unused-vars": 0 /*好み*/
  }
}
```

* webpack.config.js
```js
module.exports = {
  entry: {
    app: "./src/index.js"
  },
  output: {
    path: __dirname + '/public/js',
    filename: "[name].js"
  },
    devServer: {
    contentBase: __dirname + '/public',
    port: 8080,
    publicPath: '/js/'
  },
  devtool: "eval-source-map",
  mode: 'development',
  module: {
    rules: [{
      test: /\.js$/,
      enforce: "pre",
      exclude: /node_modules/,
      loader: "eslint-loader"
    }, {
      test: /\.css$/,
      loader: ["style-loader","css-loader"]
    }, {
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'babel-loader'
     }, {
    test: /\.(jpg|png)$/,
    loaders: 'url-loader'
    },]
  }
};
```

* public¥index.html
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta http-equiv="X-UA-Compatible" content="IE=Edge, chrome=1" />
  <title>React App</title>
</head>
<body>
  <div id="root"></div>
  <script type="text/javascript" src="js/app.js" charset="utf-8"></script>
</body>
</html>
```

4. css, jsの記述

* src/index.css
* src/index.js

5. 確認
```
npm start
```