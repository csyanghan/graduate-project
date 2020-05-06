import pymysql.cursors
from loguru import logger
import math
import json
import os

abs_path = os.path.split(os.path.realpath(__file__))[0]

logger.remove()
logger.add(os.path.join(abs_path, 'log.log'))

connection = pymysql.connect(host='cdb-om3dvlfw.cd.tencentcdb.com',
                             port=10093,
                             user='root',
                             password='mysql18817202463',
                             db='graduate-project',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def fetchItemUserLog():
  '''
  @retrun 物品-用户 的倒排表
  '''
  result = []
  try:
    with connection.cursor() as cursor:
      sql = '''
      select `user_id`, `item_id` from `behavior_log`
      '''
      cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

  except Exception as e:
    logger.error('数据库错误连接错误: ' + str(e))
  
  item_user = dict()
  for u_i in result:
    user_id = u_i['user_id']
    item_id = u_i['item_id']
    logger.info('calcute item-user:' + item_id)
    if item_id not in item_user:
      item_user[item_id] = set()
    item_user[item_id].add(user_id)
  return item_user

def fetUserItemLog():
  '''
  @retrun 用户-物品表
  '''
  result = []
  try:
    with connection.cursor() as cursor:
      sql = '''
      select `user_id`, `item_id` from `behavior_log`
      '''
      cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()

  except Exception as e:
    logger.error('数据库错误连接错误: ' + str(e))
  
  user_item = dict()
  for u_i in result:
    user_id = u_i['user_id']
    item_id = u_i['item_id']
    logger.info('calcute user-item:' + item_id)
    if user_id not in user_item:
      user_item[user_id] = set()
    user_item[user_id].add(item_id)
  for v in user_item.keys():
    user_item[v] = list(user_item[v])
  return user_item

def UserSimilarity():
  '''
  @return 用户相似度矩阵
  '''
  item_users = fetchItemUserLog()
  # item_users = {
  #   'D36003FD6CF2CEED89686A7F1F443E4E': [1,2,3],
  #   '20648E2736420F735EDC29FE9C13F243': [4,5,6]
  # }

  logger.info('物品-用户倒排表计算成功!')

  C = dict()
  N = dict()
  for _, users in item_users.items():
    for u in users:
      if u not in N: N[u] = 0
      N[u] += 1
      for v in users:
        if u == v:
          continue
        if u not in C:
          C[u] = dict()
          if v not in C[u]:
            C[u][v] = 0
        if v not in C[u]:
          C[u][v] = 0
        C[u][v] += 1
  
  W = dict()
  for u, related_users in C.items():
    for v, cuv in related_users.items():
      if u not in W:
        W[u] = dict()
      W[u][v] = cuv / math.sqrt(N[u] * N[v])
  return W

if __name__ == '__main__':
  w = UserSimilarity()
  json_w = json.dumps(w)
  with open(os.path.join(abs_path, 'w.json'), 'w') as fp:
    fp.write(json_w)
  logger.info('计算用户相似度成功!')

  ui = fetUserItemLog()
  json_ui = json.dumps(ui)
  with open(os.path.join(abs_path, 'userItem.json'), 'w') as fp:
    fp.write(json_ui)
  logger.info('计算用户-项目表成功!')
