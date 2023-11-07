from flask import Flask
from flask_smorest import Api
from resources.item import blp as itemBluePrint
from resources.user import blp as UserBluePrint
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
class MyFlask(Flask):
    def make_response(self, rv):
        if not rv:
            return super().make_response("Any String")
        return super().make_response(rv)

app = MyFlask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Item Rest api"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["JWT_SECRET_KEY"]="79661339402040034048725754551641916008"

jwt=JWTManager(app)

@jwt.token_in_blocklist_loader
def check_token_in_blocklist_loader(jwt_header,jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoke_toker_loader(jwt_header,jwt_payload):
    return(
        {
            "description":"User has been logged out",
            "error":"token revoked"
        },
        401
    )


api = Api(app)
api.register_blueprint(itemBluePrint)
api.register_blueprint(UserBluePrint)

################### Following data have been stored in item.py ##########################
#################### data is imported through from db import items ###################
"""
items = {"d21297f3769b4b37b527b7aed12b406c": {"name": "Tanuj Yadav",
                                              "No.of Balls Faced": 10,
                                            "runs": 3,
                                              "Out-Method": "Bowled"
                                              },
         "7604bfad1f684d79b4439aa287873ece": {
             "name": "Ashutosh Ranjan",
             "No.of Balls Faced": 2,
             "runs": 0,
            "Out-Method": "Stumped"

         }, "1023828301d341499a3ef13b28a3ddbf": {
        "name": "Rajesh Snehi",
        "No.of Balls Faced": 20,
        "runs": 2,
        "Out-Method": "Catch"
    }
         }
"""

"""

@app.get("/items")
#def get_items():
   # return {"items": items}


@app.get('/item')
def get_item():
    id = request.args.get('id')
    if id == None:
        return {"items":items}
    try:
         return items[id]
    except KeyError:
        return {"message": "Record doesn't exist"}

    ##for item in items:
    ##  if name == item['name']:
    ##    return item


## return {"message": "Record doesn't exist"}


@app.post('/item')
def add_item():
    request_data = request.get_json()
    #### Data validation or handling exception ##############

    if "name" not in request_data or "No.of Balls Faced" not in request_data or "runs"  not in request_data or "Out-Method" not in request_data:
        return {"message": "Please include all the entries of body"}
    items[uuid.uuid4().hex] = request_data
    ## items.append(request_data)
    return {"message": "item added successfully"}, 201


@app.put('/item')
def update_data():
    id= request.args.get('id')
    request_data = request.get_json()
    #### Data validation or handling exception ##############
    if id == None:
        return {"message":"Given ID not found"},404
    #### Data validation or handling exception ##############

    if "name" not in request_data or "No.of Balls Faced" not in request_data or "runs" not in request_data or "Out-Method" not in request_data:
         return {"message":"Please include all the entries of body"}


    if id in items.keys():
        items[id] = request_data
        return {"message": "Item added successfully"}
    else:
        return {"message": "Record doesn't exist"}
    ##for item in items:
    ##  if item['name'] == request_data['name']:
    ##    item['Run'] = request_data['Run']
    ##  return {"message": "item updated successfully"}
    ##return {"message": "Record doesn't exist"}, 200


@app.delete('/item')
def delete_items():
    id = request.args.get('id')
    #### Data validation or handling exception ##############
    if id == None:
        return {"message":"Given ID not found"}

    if id in items.keys():
        del items[id]
        return {"message":"Item deleted successfully"}
    else:
        return {"message":"Record doesn't found"}
    #  if item['name'] == name:
      #      items.remove(item)
       #     return {"message": "Item deleted successfully"}
    #return {"message": "Record doesn't exist"}, 404
"""

################### Dockerfile #################

# 1 FROM python: 3.10
# 2 EXPOSE 5000
# 3 WORKDIR / app
# 4 RUN pip install flask
# 5 COPY..
# 6 CMD ["flask", "run", "--host", "0.0.0.0"]

################### requirements.txt #################

# flask
# python-dotenv

################### .flaskenv #################

# FLASK_APP=app
# FLASK_DEBUG=1

################### text.py #################

# import uuid
# print(uuid.uuid4().hex)
