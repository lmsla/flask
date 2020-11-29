import flask
from flask import request,jsonify,make_response
from flask_restful import Api,Resource
from resource.user import Users,User
from resource.accounts import Accounts,Account
import pymysql
app = flask.Flask(__name__)
app.config["DEBUG"]=True
api =Api(app)
api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
api.add_resource(Accounts,'/Accounts')
api.add_resource(Account,'/Account/<id>')

@app.route('/' , methods = ['GET'])
def home():
  return '<h3>hello<h3>'

@app.before_request
def auth():
  token = request.headers.get('auth')
  if token == '567':
    pass
  else:
    response = {'msg':'invalid token'}
    return response , 401
@app.errorhandler(Exception)
def handle_error(error):
  status_code = 500
  if(type(error).__name__ == 'NotFound'):
    status_code = 404
  else:
    pass
  return{'msg':type(error).__name__},status_code

@app.route('/account/<account_number>/deposit',methods=['POST'])
def deposit(account_number):
  db,cursor,account = get_account(account_number)
  money =request.values['money']
  balance = account['balance']+ int(money)
  sql = """
  Update web_API.account Set balance = {}
  where account_number = '{}'
  """.format(balance,account_number)
  cursor.execute(sql)
  db.commit()
  db.close()
  response={
    'result' : True
  }
  return jsonify(response)

@app.route('/account/<account_number>/withdraw',methods=['POST'])
def withdraw(account_number):
  db,cursor,account = get_account(account_number)
  money =request.values['money']
  balance = account['balance'] - int(money)

  if balance < 0 :
    response = {
      'result':False,
      'msg': '餘額不足'
    }
    code = 400

  elif int(money) > 30000:
    return make_response(jsonify({'msg':'單次提領上限三萬'}))

  else:
    sql = """
    Update web_API.account Set balance = {}
    where account_number = '{}'
    """.format(balance,account_number)
    cursor.execute(sql)
    db.commit()
    db.close()
    response={
      'result' : True
    }
    code = 200
  return jsonify(response),code

def get_account(account_number):
  db = pymysql.connect('localhost','root','pn123456','web_API')
  cursor = db.cursor(pymysql.cursors.DictCursor)
  sql = """ Select * From web_API.account where account_number='{}'
        """.format(account_number)
  cursor.execute(sql)
  return db ,cursor ,cursor.fetchone()


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=80)