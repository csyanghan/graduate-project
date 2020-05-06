from userSimilarity import UserSimilarity, fetUserItemLog
import json
import os

abs_path = os.path.split(os.path.realpath(__file__))[0]

def getUserSimilarity():
  w_path = os.path.join(abs_path, 'w.json')
  if not os.path.exists(w_path):
    w = UserSimilarity()
    json_w = json.dumps(w)
    with open(w_path, 'w') as fp:
      fp.write(json_w)
  with open(w_path, 'r') as fp:
    w = json.loads(fp.read())
  return w

def getUserItem():
  user_item_path = os.path.join(abs_path, 'userItem.json')
  if not os.path.exists(user_item_path):
    user_item = fetUserItemLog()
    json_user_item = json.dumps(user_item)
    with open(user_item_path, 'w') as fp:
      fp.write(json_user_item)
  with open(user_item_path, 'r') as fp:
    user_item = json.loads(fp.read())
  return user_item

def userCFRecommend(user, k):
  w = getUserSimilarity()
  user_item = getUserItem()
  rank = dict()
  try:
    interacted_items = user_item[user]
  except Exception:
    return []
  
  for v, wuv in sorted(w[user].items(), key = lambda x: float(x[1]), reverse=True )[0:k]:
    for i in user_item[v]:
      if i in interacted_items:
        pass
      else:
        if i not in rank:
          rank[i] = 0
        rank[i] += wuv
  rank = sorted(rank.items(), key = lambda x: float(x[1]), reverse=True)
  return rank[0:20]

if __name__ == '__main__':
  rec = userCFRecommend('3', 10)
  print(rec)
