const Service = require('egg').Service;

class UserService extends Service {
  async save(userParams) {
    const user = await this.queryByUserName(userParams.username);
    if (user) return false;
    const result = await this.app.mysql.insert('users', { ...userParams });
    const insertSuccess = result.affectedRows === 1;
    if (insertSuccess) return this.queryByUserName(userParams.username);
    return false;
  }

  async queryByUserName(username) {
    const user = await this.app.mysql.get('users', { username });
    if (user) return user;
    return false;
  }

  async loginAndGetUser(username, password) {
    const user = await this.app.mysql.get('users', { username });
    if (!user || user.password !== password) {
      return false;
    }
    return user;
  }
}
module.exports = UserService;
