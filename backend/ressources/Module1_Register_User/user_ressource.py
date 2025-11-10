from flask import Blueprint 
from controllers.Module1_Register_User.user_controller import UserController
from flask_restful import Resource, reqparse


controller = UserController()

class RegisterUserResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('role', required=False)
        args = parser.parse_args()
        return controller.register_user(args)


class SetUserProfileResource(Resource):
    def post(self, user_id):
        parser = reqparse.RequestParser()
        # Ajoute ici tous les champs possibles pour ton profil
        parser.add_argument('first_name', required=False)
        parser.add_argument('last_name', required=False)
        parser.add_argument('title', required=False)
        parser.add_argument('description', required=False)
        parser.add_argument('company_name', required=False)
        args = parser.parse_args()
        return controller.set_user_profile(user_id, args)