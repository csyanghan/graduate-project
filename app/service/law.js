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

}
module.exports = LawService;
