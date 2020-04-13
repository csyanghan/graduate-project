const Controller = require('egg').Controller;
const moment = require('moment');

class UserController extends Controller {
  async register() {
    const { ctx } = this;
    const { username, password } = ctx.request.body;
    const newUser = {
      username,
      password,
      created_at: moment().format(),
      updated_at: moment().format(),
    };
    const user = await ctx.service.user.save(newUser);
    if (user) {
      // 设置 Session
      ctx.session.user = { id: user.id, username: user.username };
      ctx.body = {
        code: 200,
        data: user,
        msg: '注册成功',
      };
    } else {
      ctx.body = {
        code: 409,
        msg: '用户名已存在',
      };
    }
  }

  async login() {
    const { ctx } = this;
    const { username, password } = ctx.request.body;
    const user = await ctx.service.user.loginAndGetUser(username, password);
    if (!user) {
      ctx.body = {
        code: 401,
        msg: '用户名或密码错误！',
      };
    } else {
      // 设置 Session
      ctx.session.user = { id: user.id, username: user.username };
      ctx.body = {
        code: 200,
        data: user,
        msg: '登录成功!',
      };
    }
  }
}

module.exports = UserController;
