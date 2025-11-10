# [file name]: mission_ressource.py
from flask_restful import Resource, reqparse
from controllers.Module2_Client_Management.mission_controller import MissionController

controller = MissionController()

class MissionListResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('skills', type=str)
        parser.add_argument('min_budget', type=float)
        parser.add_argument('max_budget', type=float)
        args = parser.parse_args()
        
        return controller.get_all_missions(filters=args)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('budget', type=float, required=True)
        parser.add_argument('budget_type', required=True)
        parser.add_argument('deadline', required=True)
        parser.add_argument('required_skills', action='append')
        args = parser.parse_args()
        
        # Récupérer le client_id depuis l'authentification
        client_id = 1  # À remplacer par l'ID du user authentifié
        return controller.create_mission(client_id, args)

class ApplicationResource(Resource):
    def post(self, mission_id):
        parser = reqparse.RequestParser()
        parser.add_argument('proposal', required=True)
        parser.add_argument('proposed_budget', type=float)
        parser.add_argument('delivery_time')
        args = parser.parse_args()
        
        freelance_id = 1  # À remplacer par l'ID du user authentifié
        return controller.apply_to_mission(mission_id, freelance_id, args)