from sqlite3.dbapi2 import Cursor
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


#resource should be class
class Item(Resource):
    #reqparse is used to  get only desired key values from the user.
    #in this put request we only change the price, not name. In that case we only want user to send the price not the username. Thats why we use ths.
  parser=reqparse.RequestParser()
  parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"
                        )

  parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank"
                        )
  @jwt_required() #the makes sure that we get authunticate before get request
  def get(self,name):
    item=ItemModel.find_by_name(name)#returns itemModel object
    if item is not None:
        return item.json()
    return {"message":"row doesn't exist"},404

  def post(self,name):
    #need to make sure there no duplicate item.
    if ItemModel.find_by_name(name) is not None:
      return {'message': "An item with name {} is already exists.".format(name)}, 400 #bad request
    # data=request.get_json() #post request send the data to api and we store it in data
    #this will parse the arguments that come through the json payload
    data=Item.parser.parse_args() #this will return only the above proposed argument dictionary

    item=ItemModel(name,data['price'],data['store_id'])

    try:
      item.save_to_db()
    except:
      return {"message": "An error occured inserting the item."}, 500 #internal server error

    return item.json(), 201

  def delete(self,name):
    item=ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    return {'message':'item has been deleted'}

  def put(self,name):

    #this will parse the arguments that come through the json payload
    data=Item.parser.parse_args() #this will return only the above proposed argument dictionary
    # data=request.get_json() #returns dictionary
    item=ItemModel.find_by_name(name)
    if item is None:
      item=ItemModel(name,data['price'],data['store_id'])
    else:
      item.price=data['price']
      item.store_id=data['store_id']

    item.save_to_db()
      
    return item.json()

class ItemList(Resource):
  def get(self):
    return {'item':[item.json() for item in ItemModel.query.all()]}
