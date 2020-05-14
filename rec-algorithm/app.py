import jieba
import jieba.analyse
import os
from flask import Flask
from flask import request
from flask import jsonify
from loguru import logger
from userSimilarity import connection
from userCF import userCFRecommend
from itemCF import itemCFRecommend

app = Flask(__name__)
abs_path = os.path.split(os.path.realpath(__file__))[0]

logger.remove()
logger.add(os.path.join(abs_path, 'app.log'))

@app.route('/recommend', methods=['POST'])
def recommendBaseUser():
  # 基于用户的推荐
  body = request.get_json(force=True)
  user_id = body['userId']
  rank = userCFRecommend(str(user_id), 10)
  return jsonify(rank)

@app.route('/recommendBaseItem', methods=['POST'])
def recommendBaseItem():
  # 基于项目的推荐
  body = request.get_json(force=True)
  user_id = body['userId']
  rank = itemCFRecommend(str(user_id), 10)
  return jsonify(rank)

@app.route('/recommendBaseContent', methods=['POST'])
def recommendBaseContent():
  # 相似案例推荐
  # https://www.jianshu.com/p/c48106149b6a
  body = request.get_json(force=True)
  caioanyaodian = body.get('caipanyaodian')
  keywords = jieba.analyse.extract_tags(caioanyaodian, 10) # 关键词
  against = '+' + keywords[0] + ' ' + ' '.join(keywords[1:])
  sql ='''
    SELECT id, anming, caipanyaodian FROM anli
    WHERE MATCH (caipanyaodian)
    AGAINST ('{}' IN BOOLEAN MODE) limit 6;
  '''.format(against)
  result = []
  try:
    with connection.cursor() as cursor:
      cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

  except Exception as e:
    logger.error('数据库错误连接错误: ' + str(e))
  return jsonify(result)

@app.route('/index', methods=['GET'])
def index():
  return 'Hello world'

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
