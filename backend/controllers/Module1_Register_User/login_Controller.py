from flask import request, jsonify

from models.models import * 


class LoginController:
    def login(self,arg):
        user = User.query.filter_by(email=arg['email']).first()
        if user and user.check_password(arg['pass']):
            return {'message': "Login success !", "data": user.to_dict() , "token":"mon-jwt-token"},200
        else:
            return {"message": "Invalid credidential"},401
