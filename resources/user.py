import uuid
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from Database.user import UserDatabase
from Schemas import UserGetAndDeleteSchema,UserSchema,SuccessMessageSchema
from flask_jwt_extended import create_access_token, jwt_required,get_jwt
import hashlib
from blocklist import BLOCKLIST

blp=Blueprint("users",__name__,description="Operations on users")


@blp.route('/login')
class UserLogin(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UserSchema)
    def post(self,request_data):
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
        result = self.db.verify_user(username, password)
        print(result)
        if result:
            return {"access token" : create_access_token(identity=result)}
        abort(404,message="username or password is incorrect")

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti=get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully logged out"}


@blp.route('/users')
class User(MethodView):

    def __init__(self):
        self.db=UserDatabase()

    @blp.response(200,UserSchema)
    @blp.arguments(UserGetAndDeleteSchema,location="query")
    def get(self, args):
        id=args.get('id')
        result=self.db.get_user(id)
        if result is None:
            abort(404,message="Record doesn't exist")
        return result
    @blp.response(200,SuccessMessageSchema)
    @blp.arguments(UserSchema)
    def post(self,request_data):
        username = request_data["username"]
        password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()

        if self.db.add_user(username,password):
            return {"message":"User added successfully"}
        abort(403,message="User already exits")

    @blp.arguments(UserGetAndDeleteSchema,location="query")
    @blp.response(200,SuccessMessageSchema)
    def delete(self,args):
        id=args.get('id')
        if self.db.delete_user(id):
            return {"message":"User deleted"}
        abort(404,message="Given user not found")





