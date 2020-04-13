const path = require('path');

const resolve = (dir) => path.join(__dirname, dir);

module.exports = {
  devServer: {
    proxy: 'http://127.0.0.1:7001',
  },
  chainWebpack: (config) => {
    config.resolve.alias
      .set('@', resolve('src')); // key,value自行定义，比如.set('@@', resolve('src/components'))
  },
};
