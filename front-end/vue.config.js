const path = require('path');

const resolve = (dir) => path.join(__dirname, dir);

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:7001',
        changeOrigin: true,
        pathRewrite: {
          '^/api' : ''
        }
      }
    }
  },
  chainWebpack: (config) => {
    config.resolve.alias
      .set('@', resolve('src')); // key,value自行定义，比如.set('@@', resolve('src/components'))

    config.plugin('html').tap((args) => {
      args[0].title = '案例通--法律案例推荐系统'
      return args
    });
  },
};
