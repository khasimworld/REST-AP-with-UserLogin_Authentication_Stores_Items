import sqlite3
from typing import Text

from flask_restful import Resource,reqparse
from models.user import UserModel

class UserRegister(Resource):
  #reqparse is used to  get only desired key values from the user.
  #in this put request we only change the price, not name. In that case we only want user to send the price not the username. Thats why we use ths.
  parser=reqparse.RequestParser()
  parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )
  parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )
  def post(self):
    #this will parse the arguments that come through the json payload
    data=UserRegister.parser.parse_args() #this will return only the above proposed argument dictionary
    
    #check if the user already exist
    if UserModel.find_by_username(data['username']) is not None:
      return {"message":"A user with that username already exist"},400

    user=UserModel(data['username'],data['password'])
    user.save_to_db()

    return {"message":"User created SUccessfully"},201  #created


