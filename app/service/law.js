const Service = require('egg').Service;

class LawService extends Service {
  async search(keyword) {
    const sql = `
    SELECT id, name, caipanyaodian FROM anli
    WHERE MATCH (caipanyaodian)
    AGAINST ('${keyword}' IN BOOLEAN MODE)`;
    const start = new Date().getTime();
    const results = await this.app.mysql.query(sql);
    const end = new Date().getTime();
    return {
      results,
      time: (end - start) / 1000,
    };
  }

  async getLawById(id) {
    const law = await this.app.mysql.get('anli', { id });
    return law;
  }

  async getRecommendByUser() {
    const ctx = this.ctx;
    const userId = ctx.cookies.get('userId');
    if (!userId) {
      const sql = 'select * from anli order by views desc limit 9';
      const results = await this.app.mysql.query(sql);
      return {
        data: results,
        msg: 'unauthorized',
      };
    }
    const res = await ctx.curl('http://127.0.0.1:5000/recommend', {
      method: 'POST',
      data: {
        userId,
      },
      dataType: 'json',
      contentType: 'json',
    });
    return {
      data: res.data,
      msg: 'success',
    };
  }

  async getRecommendByItem() {
    const ctx = this.ctx;
    const userId = ctx.cookies.get('userId');
    if (!userId) {
      return {
        data: [],
        msg: 'unauthorized',
      };
    }
    const res = await this.app.mysql.get('users', { id: userId });
    return {
      data: res.recommend,
      msg: 'success',
    };
  }

  async getRecommendByContent(id) {
    const anli = await this.app.mysql.get('anli', { id });
    const keyword = anli.keyword;
    const sql = `
    SELECT id, anming, caipanyaodian FROM anli
    WHERE MATCH (caipanyaodian)
    AGAINST ('${keyword}' IN BOOLEAN MODE) limit 6;`;
    const results = await this.app.mysql.query(sql);
    return results;
  }
}
module.exports = LawService;
