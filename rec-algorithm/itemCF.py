import math
import json
import os
from userCF import getUserItem
from userSimilarity import connection
from loguru import logger

abs_path = os.path.split(os.path.realpath(__file__))[0]
logger.remove()
logger.add(os.path.join(abs_path, 'app.log'))

def itemSimilarity():
  item_similarity_path = os.path.join(abs_path, 'itemSimilarity.json')
  if os.path.exists(item_similarity_path):
    with open(item_similarity_path, 'r') as fp:
      item_smilarity = json.loads(fp.read())
      return item_smilarity
  user_item = getUserItem()
  C = dict()
  N = dict()
  for _, items in user_item.items():
    for i in items:
      if i not in N: N[i] = 0
      N[i] += 1
      for j in items:
        if i == j:
          continue
        if i not in C:
          C[i] = dict()
          if j not in C[i]:
            C[i][j] = 0
        if j not in C[i]:
          C[i][j] = 0
        C[i][j] += 1
  W = dict()
  for i, related_items in C.items():
    for j, cij in related_items.items():
      if i not in W:
        W[i] = dict()
      W[i][j] = cij / math.sqrt(N[i] * N[j])
  json_W = json.dumps(W)
  with open(os.path.join(abs_path, 'itemSimilarity.json'), 'w') as fp:
    fp.write(json_W)
  print('计算物品相似度成功')
  return W


def itemCFRecommend(user_id,k):
  w = itemSimilarity()
  rank = dict()
  user_item = getUserItem()
  try:
    # 新注册用户没有浏览记录
    ru = user_item[user_id]
  except Exception:
    return []
  for i in ru:
    for j, wj in sorted(w[i].items(), key = lambda x: float(x[1]), reverse=True )[0:k]:
      if j in ru:
        continue
      if j not in rank:
        rank[j] = 0
      rank[j] += wj
  
  rank = sorted(rank.items(), key = lambda x: float(x[1]), reverse=True)
  rank = map(lambda x:x[0] , rank)
  rank = ','.join(rank)
  return rank

def saveToMysql():
  sql = 'select id from users'
  result = []
  try:
    with connection.cursor() as cursor:
      cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
  except Exception as e:
    logger.error('数据连接错误-获取id失败:' + str(e))

  for user_id in result:
    logger.info('获取推荐结果:' + str(user_id))
    rank = itemCFRecommend(str(user_id.get('id')), 10)
    sql2 = """
    update users set recommend='{}' where id={}
    """.format(rank, user_id.get('id'))
    try:
      with connection.cursor() as cursor:
        cursor.execute(sql2)
      connection.commit()
      result = cursor.fetchone()
    except Exception as e:
      logger.error('数据连接错误-存入推荐结果失败:' + str(user_id), str(e))
    
if __name__ == '__main__':
  saveToMysql()
