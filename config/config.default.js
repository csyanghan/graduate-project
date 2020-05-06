/* eslint valid-jsdoc: "off" */

'use strict';
const dbConfig = require('./dbconfig').mysql;
/**
 * @param {Egg.EggAppInfo} appInfo app info
 */
module.exports = appInfo => {
  /**
   * built-in config
   * @type {Egg.EggAppConfig}
   **/
  const config = exports = {};

  // use for cookie sign key, should change to your own and keep security
  config.keys = appInfo.name + '_1586607904086_9026';

  // add your middleware config here
  config.middleware = [];

  config.mysql = {
    // 单数据库信息配置
    client: {
      // host
      host: 'cdb-om3dvlfw.cd.tencentcdb.com',
      // 端口号
      port: '10093',
      // 用户名
      user: 'root',
      // 密码
      password: dbConfig.password || 'password',
      // 数据库名
      database: 'graduate-project',
    },
    // 是否加载到 app 上，默认开启
    app: true,
    // 是否加载到 agent 上，默认关闭
    agent: false,
  };

  config.security = {
    domainWhiteList: [ '*' ],
    csrf: {
      ignoreJSON: true,
    },
  };


  // add your user config here
  const userConfig = {
    // myAppName: 'egg',
  };

  return {
    ...config,
    ...userConfig,
  };
};
