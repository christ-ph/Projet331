from flask import Blueprint 
from controllers.Module1_Register_User.freelance_controller import FreelanceController
from flask_restful import Resource, reqparse


controller = FreelanceController()

class FreelanceListResource(Resource):
    def get(self):
        return controller.get_all_profiles()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('skills', action='append')
        parser.add_argument('hourly_rate', type=float)
        parser.add_argument('availability')
        args = parser.parse_args()
        return controller.create_profile(args)


class FreelanceResource(Resource):
    def get(self, user_id):
        """Récupérer le profil freelance d’un utilisateur"""
        return controller.get_profile_by_user(user_id)  # nouvelle méthode à créer dans controller

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('skills', action='append')
        parser.add_argument('hourly_rate', type=float)
        parser.add_argument('availability')
        args = parser.parse_args()
        return controller.update_profile(user_id, args)

    def delete(self, user_id):
        return controller.delete_profile_by_user(user_id)


class PortfolioListResource(Resource):
    def get(self, profile_id):
        """Liste tous les projets d’un freelance"""
        return controller.get_portfolio_items(profile_id)

    def post(self, profile_id):
        """Ajoute un projet au portfolio"""
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="Title is required")
        parser.add_argument('description')
        parser.add_argument('project_url')
        parser.add_argument('image_url')
        args = parser.parse_args()
        return controller.add_portfolio_item(profile_id, args)


class PortfolioItemResource(Resource):
    def get(self, profile_id, item_id):
        """Récupère un projet spécifique"""
        return controller.get_portfolio_item(profile_id, item_id)

    def put(self, profile_id, item_id):
        """Met à jour un projet du portfolio"""
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('description')
        parser.add_argument('project_url')
        parser.add_argument('image_url')
        args = parser.parse_args()
        return controller.update_portfolio_item(profile_id, item_id, args)

    def delete(self, profile_id, item_id):
        """Supprime un projet du portfolio"""
        return controller.remove_portfolio_item(profile_id, item_id)
