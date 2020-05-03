from userSimilarity import UserSimilarity, fetUserItemLog
import json
import os

def getUserSimilarity():
  if not os.path.exists('w.json'):
    w = UserSimilarity()
    json_w = json.dumps(w)
    with open('w.json', 'w') as fp:
      fp.write(json_w)
  with open('w.json', 'r') as fp:
    w = json.loads(fp.read())
  return w

def getUserItem():
  if not os.path.exists('userItem.json'):
    user_item = fetUserItemLog()
    json_user_item = json.dumps(user_item)
    with open('userItem.json', 'w') as fp:
      fp.write(json_user_item)
  with open('userItem.json', 'r') as fp:
    user_item = json.loads(fp.read())
  return user_item

def userCFRecommend(user, k):
  w = getUserSimilarity()
  user_item = getUserItem()
  rank = dict()
  interacted_items = user_item[user]
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
