import requests
import pymysql.cursors
from loguru import logger
import os

abs_path = os.path.split(os.path.realpath(__file__))[0]

logger.remove()
logger.add(os.path.join(abs_path, 'spider_log.log'))

connection = pymysql.connect(host='cdb-om3dvlfw.cd.tencentcdb.com',
                             port=10093,
                             user='root',
                             password='mysql18817202463',
                             db='graduate-project',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

headers = {
  'Cookie': 'SESSION=d4091a0a-3f61-4db8-be7e-cb7ef0701ee2; _gscu_125736681=86441563fsngz620; Hm_lvt_9e03c161142422698f5b0d82bf699727=1586441565,1586571314,1586571789',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
  'Referer': 'https://anli.court.gov.cn/static/web/index.html',
}

def get_detail(id):
  try:
    url = 'https://anli.court.gov.cn/sfalw/case/altx/cases/detail/' + id
    r = requests.get(url, headers=headers)
    res = r.json()
    data = res.get('data').get('dataItem')
    anqinzaiyao = ''
    if data.get('ajzw'):
      anqinzaiyao = data.get('ajzw')
    elif data.get('jbaq'):
      anqinzaiyao = data.get('jbaq')
    return anqinzaiyao
  except Exception:
    return ''

def save_to_sql():
  sql1 = '''
  select `id` from `anli`
  '''
  result = []
  try:
    with connection.cursor() as cursor:
      cursor.execute(sql1)
    connection.commit()
    result = cursor.fetchall()

  except Exception as e:
    logger.error('数据库错误连接错误: ' + str(e))
  length = len(result)
  for i in range(length-20326, 10000, -1):
    law = result[i]
    law_id = law.get('id')
    if law_id:
      anqinzaiyao = get_detail(law_id)
      if not anqinzaiyao:
        logger.error('crawl' + str(law_id) + 'error')
        continue
      sql2 = '''
      update `anli` set `anqinzaiyao`= (%s) where `id`=(%s)
      '''
      try:
        with connection.cursor() as cursor:
          cursor.execute(sql2, (anqinzaiyao, law_id))
        connection.commit()
        r = cursor.fetchone()
        logger.success('crawl' + str(law_id) + 'success')

      except Exception as e:
        logger.error('crawl' + str(law_id) + 'error')

if __name__ == '__main__':
  save_to_sql()

