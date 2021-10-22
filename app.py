from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

#RUN CREATE TABLE FIRST************************************************************************************
#json web token

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'#we are saying that sqlalmy database is in root folder of this project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #setting flask sqlalchemy tracking to No, but it doesn't stop the Imported SQLalchemy tracking.
app.secret_key='password'
api=Api(app)

#creates tables before the first request
@app.before_first_request 
def create_tables():
  db.create_all()



# JWT createa a new end point /auth.
# by usng /auth endpoint authunticate function uses the usernamme and password to generate jw token
# we send that particular jw token when we send another request to API.
# when we send the jwtoken, JWT call the identity function and gets userid and returnt he user that reprasents the id

jwt = JWT(app,authenticate,identity) #/auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(StoreList,'/stores')


# whaever file we run that'll become __main__ 
if __name__=='__main__':
  db.init_app(app)
  app.run(port=5000,debug=True)

