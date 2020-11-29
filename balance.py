import flask
from flask import request

from flask_restful import Api,Resource
from resource.user import Users,User
app = flask.Flask(__name__)
app.config["DEBUG"]=True
api =Api(app)
api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=80)