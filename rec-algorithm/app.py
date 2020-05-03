from flask import Flask
from flask import request
from flask import jsonify
from userCF import userCFRecommend
app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommendBaseUser():
  body = request.get_json(force=True)
  user_id = body['userId']
  rank = userCFRecommend(str(user_id), 10)
  return jsonify(rank)

@app.route('/index', methods=['GET'])
def index():
  return 'Hello world'
