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

  async getLawById() {
    const { ctx } = this;
    const { id } = ctx.query;
    const res = await ctx.service.law.getLawById(id);
    ctx.body = {
      code: 200,
      data: res,
    };
  }

  async getRecommendByUser() {
    const { ctx } = this;
    const rec = await ctx.service.law.getRecommndById();
    if (rec.msg === 'unauthorized') {
      ctx.body = {
        code: 200,
        data: [],
      };
    } else {
      const law = [];
      const l = rec.data.length;
      for (let i = 0; i < l; i++) {
        const detail = await ctx.service.law.getLawById(rec.data[i][0]);
        detail.similarity = rec.data[i][1];
        law.push(detail);
      }
      ctx.body = {
        code: 200,
        data: law,
      };
    }
  }
}

module.exports = LawController;
