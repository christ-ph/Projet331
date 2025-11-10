# [file name]: mission_controller.py
from flask import request, jsonify
from models.models import db, Mission, Application, ApplicationStatus

class MissionController:
    
    def get_all_missions(self, filters=None):
        query = Mission.query.filter_by(status='PUBLISHED')
        
        if filters:
            if filters.get('skills'):
                query = query.filter(Mission.required_skills.contains(filters['skills']))
            if filters.get('min_budget'):
                query = query.filter(Mission.budget >= filters['min_budget'])
            if filters.get('max_budget'):
                query = query.filter(Mission.budget <= filters['max_budget'])
        
        missions = query.all()
        return [mission.to_dict() for mission in missions], 200

    def create_mission(self, client_id, data):
        mission = Mission(client_id=client_id, **data)
        db.session.add(mission)
        db.session.commit()
        return mission.to_dict(), 201

    def apply_to_mission(self, mission_id, freelance_id, data):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404
        
        # Vérifier si déjà postulé
        existing_application = Application.query.filter_by(
            mission_id=mission_id, 
            freelance_id=freelance_id
        ).first()
        
        if existing_application:
            return {"message": "You have already applied to this mission"}, 400
        
        application = Application(
            mission_id=mission_id,
            freelance_id=freelance_id,
            **data
        )
        
        db.session.add(application)
        db.session.commit()
        return application.to_dict(), 201