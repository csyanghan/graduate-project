const Mock = require('mockjs');
const moment = require('moment');
const mysql = require('mysql2');
const winston = require('winston');
const logger = winston.createLogger({
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'fake.log' }),
  ],
});

const pool = mysql.createPool({
  host: '106.13.174.41',
  user: 'root',
  database: 'graduate-project',
  password: '18817202463',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});
const promisePool = pool.promise();

async function getAllLawId() {
  const sql_getAllId = 'select id from anli';
  const [ rows ] = await promisePool.query(sql_getAllId);
  return rows.map(law => law.id);
}

async function insertUser() {
  const user = Mock.mock({
    username: '@word(10)',
    password: '@word(10)',
    created_at: moment().format(),
    updated_at: moment().format(),
  });
  const sql = 'insert into `users` (`username`, `password`, `created_at`, `updated_at`) values (?, ?, ?, ?)';
  const [ rows ] = await promisePool.execute(sql, [ user.username, user.password, user.created_at, user.updated_at ]);
  return rows.insertId;
}

async function fakeUserBrowseData(user, allLawId, length) {
  let browseLaws = Math.floor(Math.random() * 500); // 每个人最多浏览2k个案例
  let userId = 0;
  if (user) userId = user.id;
  else userId = await insertUser();
  logger.info(`user: ${userId} , browser: ${browseLaws} laws`)
  while (browseLaws > 0) {
    browseLaws--;
    const i = Math.floor(Math.random() * length);
    const lawId = allLawId[i];
    const sql = 'insert into `behavior_log` (`user_id`, `item_id`) values (?, ?)';
    await promisePool.execute(sql, [ userId, lawId ]);
  }
}

async function fakeAll() {
  const allLawId = await getAllLawId();
  const length = allLawId.length;
  let p = 500;
  while (p > 0) {
    p--;
    try {
      await fakeUserBrowseData(null, allLawId, length);
    } catch (e) {
      logger.error('error:' + e);
    }
  }
  logger.info('fake all');
}
fakeAll();
