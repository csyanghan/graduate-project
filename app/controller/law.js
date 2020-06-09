const Controller = require('egg').Controller;

class LawController extends Controller {
  // 搜索
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

  // 根据id查案例 并且插入一条浏览记录
  async getLawById() {
    const { ctx } = this;
    const { id, userId } = ctx.query;
    if (userId) {
      await this.app.mysql.insert('behavior_log', { user_id: userId, item_id: id });
    }
    const res = await ctx.service.law.getLawById(id);
    const recommend = await ctx.service.law.getRecommendByContent(id);
    res.recommend = recommend;
    ctx.body = {
      code: 200,
      data: res,
    };
  }

  // 基于用户的推荐: 通过用户的浏览记录判断用户之间的相似度
  async getRecommendByUser() {
    const { ctx } = this;
    const rec = await ctx.service.law.getRecommendByUser();
    if (rec.msg === 'unauthorized') {
      // 推荐热门案例
      ctx.body = {
        code: 200,
        data: rec.data,
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

  // 基于项目的推荐：通过用户的浏览记录判断项目之间的相似度 -> 喜欢a的用户大多数也喜欢b ： a b 比较相似
  async getRecommendByItem() {
    const { ctx } = this;
    const rec = await ctx.service.law.getRecommendByItem();
    if (rec.msg === 'unauthorized') {
      // 不推荐
      ctx.body = {
        code: 200,
        data: [],
      };
    } else {
      rec.data = rec.data.split(',').slice(0, 6);
      const law = [];
      const l = rec.data.length;
      for (let i = 0; i < l; i++) {
        const detail = await ctx.service.law.getLawById(rec.data[i]);
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
