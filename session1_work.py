from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pm"
mongo = PyMongo(app)
api=Api(app)


########################################### Display all user #######################################
# @app.route('/user/alluser', methods=['GET'])
class All_user(Resource):
    def post(self):
        user = mongo.db.user

        output = []

        for all_data in user.find():
            output.append({'username' : all_data['username'], 'email' : all_data['email']})

        return jsonify({'result' : output})


######################################### LOGIN #############################################
# @app.route('/user/login', methods=['POST'])
class Login(Resource):
    def post(self):
        user = mongo.db.user
        # username = request.json['name']
        # email = request.json['email']
        password = request.json['password']
        usernameORemail = request.json['usernameORemail']
        # return jsonify({"username":username})
        # return jsonify({"email":email})

        # if email:
            # login = user.find_one({"password":password,"email":email})
            # if login:
            #     output = {'username' : q['username']}
            # else:
            #     output='password or emailid wrong'
            # return jsonify({'result' : output})
        # elif username:
        #     login = user.find_one({"password":password,"username":"pundrik"})
        #     if login:
        #         output = {'username' : login['username']}
        #     else:
        #         # output = 'No results found'
        #         output='password or username wrong'
        #     return jsonify({'result' : output})

            
        login = user.find_one({
            "$or":[{"username":usernameORemail},{"email":usernameORemail}],
            "password":password
            })
        if login:
            output = {'username' : login['username']}
        else:
            output='password or username or emailid wrong'
        return jsonify({'result' : output})

####################################### REGISTER ##########################################
# @app.route('/user/register', methods=['POST'])
class Register(Resource):
    def post(self):
        user = mongo.db.user
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        newuser_id = user.insert({"username":username,"email":email,"password":password})
        newuser = user.find_one({"_id":newuser_id})
        output = {"name":newuser['username'],"email":newuser["email"],"password":newuser['password']}
        return jsonify({"new user data":output})

######################################### UPDATE PASSWORD #################################
# @app.route('/user/update', methods=['POST'])
class Update(Resource):
    def post(self):
        user = mongo.db.user
        current_password = request.json['current_password']
        new_password = request.json['new_password']
        # return jsonify({"new_password":new_password})
        current_usernameORemail = request.json['current_usernameORemail']
        user_up_id=user.update(
            {"$and":
                [
                    {"password":current_password},
                    {"$or":[{"username":current_usernameORemail},{"email":current_usernameORemail}]}   
                ]
            },
            {"$set":{"password":new_password}}
            )
        # if user_up_id:
        #     return jsonify({"result":user_up_id})
        # else:
        #     return jsonify({"result":"notupdated"})
        user_up= user_up_id["updatedExisting"]
        if (user_up== True):
            a=user_up_id["nModified"]
            if (a==1):
                return jsonify({"result":"updated password"})
            else:
                return jsonify({"result":"updated but same password entered again"})
        else:
            return jsonify({"result":"not updated"})
        
        # u_up= user.find_one({"_id":u_up_id})
        # if u_up:
        #     p={"username":u_up['username']}
        # else:
        #     p='not update'
        # return jsonify({'result':p})


api.add_resource(All_user, '/alluser')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Update, '/update')



if __name__ == '__main__':
    app.run(debug=True, port=8080)