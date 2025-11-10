from flask import Blueprint 
from controllers.Module1_Register_User.login_Controller import LoginController
from flask_restful import Resource, reqparse


controller = LoginController()


class ConnectionUserResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('pass')
        args = parser.parse_args()
        return controller.login(args)

