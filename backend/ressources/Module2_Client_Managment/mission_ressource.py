from flask_restful import Resource, reqparse
from flask import request
from controllers.Module2_Client_Management.mission_controller import MissionController

controller = MissionController()

# --- Authentification simplifiée ---
def get_authenticated_user_id():
    """Récupère l'ID utilisateur depuis le header 'User-ID'."""
    user_id = request.headers.get('User-ID')
    try:
        return int(user_id) if user_id else None
    except ValueError:
        return None

# --- Resources ---
class MissionListResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('skills', type=str, location='args')
        parser.add_argument('min_budget', type=float, location='args')
        parser.add_argument('max_budget', type=float, location='args')
        parser.add_argument('status', type=str, location='args', default='PUBLISHED')
        args = parser.parse_args()

        filters = {k: v for k, v in args.items() if v is not None}
        return controller.get_all_missions(filters=filters)

    def post(self):
        client_id = get_authenticated_user_id()
        if not client_id:
            return {"message": "Authentication required"}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str, required=True, help='Description is required')
        parser.add_argument('budget', type=float, required=True, help='Budget is required')
        parser.add_argument('budget_type', type=str, required=True, help='Budget type is required')
        parser.add_argument('deadline', type=str, required=True, help='Deadline is required')
        parser.add_argument('required_skills', type=list, location='json', default=[])
        parser.add_argument('status', type=str, default='DRAFT')
        args = parser.parse_args()

        return controller.create_mission(client_id, args)


class MissionResource(Resource):
    def get(self, mission_id):
        return controller.get_mission_by_id(mission_id)

    def put(self, mission_id):
        client_id = get_authenticated_user_id()
        if not client_id:
            return {"message": "Authentication required"}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('budget', type=float)
        parser.add_argument('budget_type', type=str)
        parser.add_argument('deadline', type=str)
        parser.add_argument('required_skills', type=list, location='json')
        parser.add_argument('status', type=str)
        args = parser.parse_args()

        update_data = {k: v for k, v in args.items() if v is not None}
        return controller.update_mission(mission_id, client_id, update_data)

    def delete(self, mission_id):
        client_id = get_authenticated_user_id()
        if not client_id:
            return {"message": "Authentication required"}, 401

        return controller.delete_mission(mission_id, client_id)


class ApplicationResource(Resource):
    def post(self, mission_id):
        freelance_id = get_authenticated_user_id()
        if not freelance_id:
            return {"message": "Authentication required"}, 401

        parser = reqparse.RequestParser()
        parser.add_argument('proposal', type=str, required=True, help='Proposal is required')
        parser.add_argument('proposed_budget', type=float)
        parser.add_argument('delivery_time', type=str)
        args = parser.parse_args()

        return controller.apply_to_mission(mission_id, freelance_id, args)


class UserMissionsResource(Resource):
    def get(self, user_id):
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        if authenticated_id != user_id:
            return {"message": "Access denied"}, 403

        return controller.get_user_missions(user_id)


class UserApplicationsResource(Resource):
    def get(self, user_id):
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        if authenticated_id != user_id:
            return {"message": "Access denied"}, 403

        return controller.get_user_applications(user_id)
