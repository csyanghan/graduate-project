const Service = require('egg').Service;

class LawService extends Service {
  async search(keyword) {
    const sql = `select * from anli where caipanyaodian like '%${keyword}%'`;
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

  async getRecommndById() {
    const ctx = this.ctx;
    const userId = ctx.cookies.get('userId');
    if (!userId) {
      return {
        data: [],
        msg: 'unauthorized',
      };
    }
    const res = await ctx.curl('http://106.13.174.41:5000/recommend', {
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
}
module.exports = LawService;
