import uuid
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from Schemas import ItemSchema
from Database.item import ItemDatabase
from Schemas import ItemGetSchema,SuccessMessageSchema,ItemOptionalQuerySchema,ItemQueryParameters
from flask_jwt_extended import jwt_required

blp = Blueprint("items", __name__, description="Operations on Item")


@blp.route('/item')
class Item(MethodView):

    def __init__(self):
        self.db=ItemDatabase()


    @blp.response(200, ItemGetSchema(many=True))
    @blp.arguments(ItemOptionalQuerySchema, location="query")
    def get(self, args):
        id = args.get('id')
        if id is None:
            return self.db.get_Items()
        else:
            result= self.db.get_Item(id)
            if result is None:
                abort(404, message="Record doesn't exist")
            else:
                return result


    @blp.arguments(ItemSchema)
    @blp.response(200,SuccessMessageSchema)
    def post(self, request_data):
        # request_data = request.get_json()
        #### Data validation or handling exception ##############
        """
        if "name" not in request_data or "No.of Balls Faced" not in request_data or "runs" not in request_data or "Out-Method" not in request_data:
            return {"message": "Please include all the entries of body"}
        """
        id = uuid.uuid4().hex
        self.db.add_Item(id,request_data)
        #items.append(item)
        ## items.append(request_data)
        return {"message": "item added successfully"}, 201


    @blp.arguments(ItemSchema)
    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(ItemQueryParameters,location="query")
    def put(self, request_data,args):
        id = args.get('id')
        #### Data validation or handling exception ##############
        if id is None:
            return {"message": "Given ID not found"}, 404
        #### Data validation or handling exception ##############

        #  if "name" not in request_data or "No.of Balls Faced" not in request_data or "runs" not in request_data or "Out-Method" not in request_data:
        # return {"message": "Please include all the entries of body"}

        if self.db.update_Item(id,request_data):
            return {"message": "Item updated successfully"}
        abort(404,message="Record doesn't exist")
        ##for item in items:
        ##  if item['name'] == request_data['name']:
        ##    item['Run'] = request_data['Run']
        ##  return {"message": "item updated successfully"}
        ##return {"message": "Record doesn't exist"}, 200

    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(ItemQueryParameters,location="query")
    def delete(self,args):
        id = args.get('id')
        #### Data validation or handling exception ##############
        if id is None:
            return {"message": "Given ID not found"}

        #if id in items.keys():
         #   del items[id]
          #  return {"message": "Item deleted successfully"}
        #else:
            #return {"message": "Record doesn't found"}
        if self.db.delete_Item(id):
        #for item in items:
         #   if item['id'] == id:
          #      items.remove(item)
            return {"message":"Item deleted"}
        abort(404,message="Record doesn't exist")
        #  if item['name'] == name:
        #      items.remove(item)
        #     return {"message": "Item deleted successfully"}
        # return {"message": "Record doesn't exist"}, 404
