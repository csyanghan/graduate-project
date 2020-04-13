const Controller = require('egg').Controller;

class LawController extends Controller {
  async search() {
    const { ctx } = this;
    const { keyword } = ctx.request.body;
    const res = await ctx.service.law.search(keyword);
    ctx.body = {
      code: 200,
      data: res.results.slice(0, 9),
      length: res.results.length,
      time: res.time,
    };
  }
}

module.exports = LawController;
