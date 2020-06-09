import jieba
import jieba.analyse
from userSimilarity import connection
from loguru import logger
import os

abs_path = os.path.split(os.path.realpath(__file__))[0]
logger.remove()
logger.add(os.path.join(abs_path, 'keyword.log'))

def get_all_anli_id_and_caipanyaodian():
  sql = '''
  select id, caipanyaodian from anli limit 50000 offset 23023
  '''
  result = []
  try:
    with connection.cursor() as cursor:
      cursor.execute(sql)
    connection.commit()
    result = cursor.fetchall()
  except Exception as e:
    print('数据连接错误-获取id失败:' + str(e))
  print('get all anli success')
  return result

def extract_keyword(anli):
  keywords = jieba.analyse.extract_tags(anli['caipanyaodian'], 10) # 关键词
  against = ''
  if len(keywords) == 1:
    against = '+' + keywords[0]
  if len(keywords) > 1:
    against = '+' + keywords[0] + ' ' + ' '.join(keywords[1:])
  return against

def saveToMysql():
  allAnli = get_all_anli_id_and_caipanyaodian()
  for anli in allAnli:
    keyword = extract_keyword(anli)
    sql = '''
    update anli set keyword='{}' where id='{}'
    '''.format(keyword, anli['id'])
    try:
      with connection.cursor() as cursor:
        cursor.execute(sql)
      connection.commit()
      cursor.fetchone()
      logger.info('extract success: {}'.format(anli['id']))
    except Exception as e:
      print('数据连接错误-存入推荐结果失败:' + str(e))

if __name__ == '__main__':
  saveToMysql()
