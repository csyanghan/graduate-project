'use strict';

/**
 * @param {Egg.Application} app - egg application
 */
module.exports = app => {
  const { router, controller } = app;
  router.get('/', controller.home.index);
  router.post('/user/register', controller.user.register);
  router.post('/user/login', controller.user.login);
  router.post('/law/search', controller.law.search);
  router.get('/law/getLawById', controller.law.getLawById);
  router.get('/law/recommend', controller.law.getRecommendByUser);
  router.get('/law/recommendByItem', controller.law.getRecommendByItem);
  router.get('/user/userInfo', controller.user.getUserInfo);
};
