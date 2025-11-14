from datetime import datetime
from flask import request
from models.models import db, Mission, Application, MissionStatus, ApplicationStatus

class MissionController:

    def get_all_missions(self, filters=None):
        query = Mission.query

        # Filtre par statut par défaut
        status = filters.get('status', 'PUBLISHED') if filters else 'PUBLISHED'
        query = query.filter(Mission.status == MissionStatus(status))

        # Filtres optionnels
        if filters:
            if 'skills' in filters:
                query = query.filter(Mission.required_skills.contains([filters['skills']]))
            if 'min_budget' in filters:
                query = query.filter(Mission.budget >= filters['min_budget'])
            if 'max_budget' in filters:
                query = query.filter(Mission.budget <= filters['max_budget'])

        missions = query.all()
        # ⚡ Toujours retourner un dict pour Flask-RESTful
        return {"missions": [mission.to_dict() for mission in missions]}, 200

    def get_mission_by_id(self, mission_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404
        return {"mission": mission.to_dict()}, 200

    def create_mission(self, client_id, data):
        try:
            deadline = datetime.fromisoformat(data['deadline'])
            required_skills = data.get('required_skills', [])
            status = MissionStatus(data.get('status', 'DRAFT'))

            mission = Mission(
                title=data['title'],
                description=data['description'],
                budget=data['budget'],
                budget_type=data.get('budget_type', 'FIXED'),
                deadline=deadline,
                client_id=client_id,
                required_skills=required_skills,
                status=status
            )

            db.session.add(mission)
            db.session.commit()
            return {"mission": mission.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error creating mission: {str(e)}"}, 500

    def update_mission(self, mission_id, client_id, data):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404

        if mission.client_id != client_id:
            return {"message": "Access denied"}, 403

        try:
            if 'deadline' in data:
                data['deadline'] = datetime.fromisoformat(data['deadline'])
            if 'status' in data:
                data['status'] = MissionStatus(data['status'])
            if 'required_skills' in data and not isinstance(data['required_skills'], list):
                data['required_skills'] = list(data['required_skills'])

            for key, value in data.items():
                setattr(mission, key, value)

            db.session.commit()
            return {"mission": mission.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating mission: {str(e)}"}, 500

    def delete_mission(self, mission_id, client_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404

        if mission.client_id != client_id:
            return {"message": "Access denied"}, 403

        try:
            db.session.delete(mission)
            db.session.commit()
            return {"message": "Mission deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error deleting mission: {str(e)}"}, 500

    def apply_to_mission(self, mission_id, freelance_id, data):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404

        if mission.status != MissionStatus.PUBLISHED:
            return {"message": "Cannot apply to this mission"}, 400

        existing = Application.query.filter_by(
            mission_id=mission_id,
            freelance_id=freelance_id
        ).first()
        if existing:
            return {"message": "You have already applied"}, 400

        try:
            application = Application(
                mission_id=mission_id,
                freelance_id=freelance_id,
                status=ApplicationStatus.PENDING,
                proposal=data['proposal'],
                proposed_budget=data.get('proposed_budget'),
                delivery_time=data.get('delivery_time')
            )
            db.session.add(application)
            db.session.commit()
            return {"application": application.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error applying: {str(e)}"}, 500

    def get_user_missions(self, user_id):
        missions = Mission.query.filter_by(client_id=user_id).all()
        return {"missions": [m.to_dict() for m in missions]}, 200

    def get_user_applications(self, user_id):
        applications = Application.query.filter_by(freelance_id=user_id).all()
        return {"applications": [a.to_dict() for a in applications]}, 200
