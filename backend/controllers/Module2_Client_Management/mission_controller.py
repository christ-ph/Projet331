from datetime import datetime
from flask import request
from models.models import (
    User, UserRole, db,
    Mission, MissionStatus,
    Application, ApplicationStatus
)

class MissionController:

    # -------------------------------------------------------
    # 🔹 GET ALL MISSIONS WITH FILTERS
    # -------------------------------------------------------
    def get_all_missions(self, filters=None):
        query = Mission.query

        # Statut par défaut
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
        return {"missions": [mission.to_dict() for mission in missions]}, 200

    # -------------------------------------------------------
    # 🔹 GET MISSION BY ID
    # -------------------------------------------------------
    def get_mission_by_id(self, mission_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404
        return {"mission": mission.to_dict()}, 200

    # -------------------------------------------------------
    # 🔹 CREATE MISSION
    # -------------------------------------------------------
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

    # -------------------------------------------------------
    # 🔹 UPDATE MISSION
    # -------------------------------------------------------
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

    # -------------------------------------------------------
    # 🔹 DELETE MISSION
    # -------------------------------------------------------
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

    # -------------------------------------------------------
    # 🔹 APPLY TO MISSION
    # -------------------------------------------------------
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

    # -------------------------------------------------------
    # 🔹 GET USER MISSIONS
    # -------------------------------------------------------
    def get_user_missions(self, user_id):
        missions = Mission.query.filter_by(client_id=user_id).all()
        return {"missions": [m.to_dict() for m in missions]}, 200

    # -------------------------------------------------------
    # 🔹 GET USER APPLICATIONS
    # -------------------------------------------------------
    def get_user_applications(self, user_id):
        applications = Application.query.filter_by(freelance_id=user_id).all()
        return {"applications": [a.to_dict() for a in applications]}, 200

    # -------------------------------------------------------
    # 🔹 LAST OFFERS
    # -------------------------------------------------------
    def get_last_offres(self):
        last_offers = Mission.query.filter_by(
            status=MissionStatus.PUBLISHED
        ).order_by(
            Mission.created_at.desc()
        ).limit(10).all()

        return {"last_offers": [m.to_dict() for m in last_offers]}, 200

    # -------------------------------------------------------
    # 🔹 GET FREELANCE MISSIONS
    # -------------------------------------------------------
    def get_freelance_missions(self, user_id):
        mission_freelance = Mission.query.join(Application)\
                                         .filter(Application.freelance_id == user_id).all()
        return {"missions_freelance": [m.to_dict() for m in mission_freelance]}, 200

    # -------------------------------------------------------
    # 🔹 RECOMMENDED FREELANCERS
    # -------------------------------------------------------
    def get_recommended_freelancers(self, mission_id):
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404

        required_skills = set(mission.required_skills)

        # 🔥 ENUM corrigé
        freelances = User.query.filter_by(role=UserRole.FREELANCE).all()

        scored_freelancers = []
        for freelance in freelances:
            # FIX: Replace 'skills' with the correct attribute name from your User model
            # Common alternatives: user_skills, skill_list, etc.
            freelance_skills = set(freelance.user_skills) if hasattr(freelance, 'user_skills') else set()
            score = len(required_skills.intersection(freelance_skills))

            if score > 0:
                scored_freelancers.append({
                    "freelancer": freelance.to_dict(),
                    "score": score
                })

        scored_freelancers.sort(key=lambda x: x["score"], reverse=True)

        return {"recommended_freelancers": scored_freelancers[:10]}, 200

    # -------------------------------------------------------
    # 🔹 CLIENT MISSIONS WITH APPLICATIONS
    # -------------------------------------------------------
    def get_missions_client_applied_by_freelance(self, client_id):
        try:
            missions = Mission.query.filter_by(client_id=client_id).all()
            if not missions:
                return {"missions_with_applications": []}, 200

            missions_with_apps = []

            for mission in missions:
                applications = Application.query.filter_by(mission_id=mission.id).all()

                mission_data = {
                    "id": mission.id,
                    "title": mission.title,
                    "description": mission.description,
                    "status": mission.status.value if mission.status else None,
                    "created_at": mission.created_at.isoformat() if mission.created_at else None,
                    "applications": []
                }

                for app in applications:
                    mission_data["applications"].append({
                        "id": app.id,
                        "freelance_id": app.freelance_id,
                        "freelance_name": app.freelancer.name if app.freelancer else "Unknown",
                        "proposal": app.proposal,
                        "proposed_budget": app.proposed_budget,
                        "status": app.status.value if app.status else None,  # FIX ENUM
                        "created_at": app.created_at.isoformat() if app.created_at else None
                    })

                mission_data["applications_count"] = len(mission_data["applications"])

                missions_with_apps.append(mission_data)

            return {
                "missions_with_applications": missions_with_apps,
                "total_missions": len(missions_with_apps),
                "total_applications": sum(m["applications_count"] for m in missions_with_apps)
            }, 200

        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 500

    # -------------------------------------------------------
    # 🔹 APPLICATIONS FOR A MISSION
    # -------------------------------------------------------
    def get_mission_applications(self, mission_id):
        try:
            applications = Application.query.filter_by(mission_id=mission_id).all()
            if not applications:
                return {"applications": []}, 200

            applications_data = [
                {
                    'id': app.id,
                    'freelance_id': app.freelance_id,
                    'freelance_name': app.freelancer.name if app.freelancer else 'Unknown',
                    'freelance_email': app.freelancer.email if app.freelancer else 'Unknown',
                    'proposal': app.proposal,
                    'proposed_budget': app.proposed_budget,
                    'status': app.status,
                    'created_at': app.created_at.isoformat() if app.created_at else None,
                    'freelancer_rating': app.freelancer.rating if app.freelancer else None,
                    'freelancer_reviews_count': app.freelancer.reviews_count if app.freelancer else 0
                }
                for app in applications
            ]

            return {
                "applications": applications_data,
                "total_applications": len(applications_data)
            }, 200

        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 500







# from datetime import datetime
# from flask import request
# from models.models import User, db, Mission, Application, MissionStatus, ApplicationStatus

# class MissionController:

#     def get_all_missions(self, filters=None):
#         query = Mission.query

#         # Filtre par statut par défaut
#         status = filters.get('status', 'PUBLISHED') if filters else 'PUBLISHED'
#         query = query.filter(Mission.status == MissionStatus(status))

#         # Filtres optionnels
#         if filters:
#             if 'skills' in filters:
#                 query = query.filter(Mission.required_skills.contains([filters['skills']]))
#             if 'min_budget' in filters:
#                 query = query.filter(Mission.budget >= filters['min_budget'])
#             if 'max_budget' in filters:
#                 query = query.filter(Mission.budget <= filters['max_budget'])

#         missions = query.all()
#         # ⚡ Toujours retourner un dict pour Flask-RESTful
#         return {"missions": [mission.to_dict() for mission in missions]}, 200

#     def get_mission_by_id(self, mission_id):
#         mission = Mission.query.get(mission_id)
#         if not mission:
#             return {"message": "Mission not found"}, 404
#         return {"mission": mission.to_dict()}, 200

#     def create_mission(self, client_id, data):
#         try:
#             deadline = datetime.fromisoformat(data['deadline'])
#             required_skills = data.get('required_skills', [])
#             status = MissionStatus(data.get('status', 'DRAFT'))

#             mission = Mission(
#                 title=data['title'],
#                 description=data['description'],
#                 budget=data['budget'],
#                 budget_type=data.get('budget_type', 'FIXED'),
#                 deadline=deadline,
#                 client_id=client_id,
#                 required_skills=required_skills,
#                 status=status
#             )

#             db.session.add(mission)
#             db.session.commit()
#             return {"mission": mission.to_dict()}, 201
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"Error creating mission: {str(e)}"}, 500

#     def update_mission(self, mission_id, client_id, data):
#         mission = Mission.query.get(mission_id)
#         if not mission:
#             return {"message": "Mission not found"}, 404

#         if mission.client_id != client_id:
#             return {"message": "Access denied"}, 403

#         try:
#             if 'deadline' in data:
#                 data['deadline'] = datetime.fromisoformat(data['deadline'])
#             if 'status' in data:
#                 data['status'] = MissionStatus(data['status'])
#             if 'required_skills' in data and not isinstance(data['required_skills'], list):
#                 data['required_skills'] = list(data['required_skills'])

#             for key, value in data.items():
#                 setattr(mission, key, value)

#             db.session.commit()
#             return {"mission": mission.to_dict()}, 200
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"Error updating mission: {str(e)}"}, 500

#     def delete_mission(self, mission_id, client_id):
#         mission = Mission.query.get(mission_id)
#         if not mission:
#             return {"message": "Mission not found"}, 404

#         if mission.client_id != client_id:
#             return {"message": "Access denied"}, 403

#         try:
#             db.session.delete(mission)
#             db.session.commit()
#             return {"message": "Mission deleted successfully"}, 200
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"Error deleting mission: {str(e)}"}, 500

#     def apply_to_mission(self, mission_id, freelance_id, data):
#         mission = Mission.query.get(mission_id)
#         if not mission:
#             return {"message": "Mission not found"}, 404

#         if mission.status != MissionStatus.PUBLISHED:
#             return {"message": "Cannot apply to this mission"}, 400

#         existing = Application.query.filter_by(
#             mission_id=mission_id,
#             freelance_id=freelance_id
#         ).first()
#         if existing:
#             return {"message": "You have already applied"}, 400

#         try:
#             application = Application(
#                 mission_id=mission_id,
#                 freelance_id=freelance_id,
#                 status=ApplicationStatus.PENDING,
#                 proposal=data['proposal'],
#                 proposed_budget=data.get('proposed_budget'),
#                 delivery_time=data.get('delivery_time')
#             )
#             db.session.add(application)
#             db.session.commit()
#             return {"application": application.to_dict()}, 201
#         except Exception as e:
#             db.session.rollback()
#             return {"message": f"Error applying: {str(e)}"}, 500

#     def get_user_missions(self, user_id):
#         missions = Mission.query.filter_by(client_id=user_id).all()
#         return {"missions": [m.to_dict() for m in missions]}, 200

#     def get_user_applications(self, user_id):
#         applications = Application.query.filter_by(freelance_id=user_id).all()
#         return {"applications": [a.to_dict() for a in applications]}, 200
    
#     def get_last_offres(self):
#         last_offers = Mission.query.filter_by(status=MissionStatus.PUBLISHED).order_by(Mission.created_at.desc()).limit(10).all()

#         return { "last_offers": [m.to_dict() for m in last_offers] }, 200

#     # missions pour un freelance
#     def get_freelance_missions(self, user_id):
#         mission_freelance = Mission.query.join(Application).filter(Application.freelance_id == user_id).all()
#         return {"missions_freelance": [m.to_dict() for m in mission_freelance]}, 200
#      # recommander des freelances pour une mission donnée logique ✔️ Compare les compétences freelance ↔ mission
#     # recommander des freelances pour une mission donnée logique ✔️ Compare les compétences freelance ↔ mission
#     # ✔️ Compare les compétences freelance ↔ mission
#     # ✔️ Calcule un score selon le nombre de compétences en commun
#     # ✔️ Trie les freelances les plus pertinents
#     # ✔️ Retourne les 10 meilleurs freelances
#     def get_recommended_freelancers(self, mission_id):
#         mission = Mission.query.get(mission_id)
#         if not mission:
#             return {"message": "Mission not found"}, 404

#         required_skills = set(mission.required_skills)

#         # Récupérer tous les freelances avec leurs compétences
#         freelances = User.query.filter_by(role="FREELANCE").all()

#         scored_freelancers = []
#         for freelance in freelances:
#             freelance_skills = set(freelance.skills)
            
#             # Score = nombre de compétences en commun
#             match_score = len(required_skills.intersection(freelance_skills))

#             if match_score > 0:
#                 scored_freelancers.append({
#                     "freelancer": freelance.to_dict(),
#                     "score": match_score
#                 })

#         # Trier par pertinence
#         scored_freelancers.sort(key=lambda x: x["score"], reverse=True)

#         return {
#             "recommended_freelancers": scored_freelancers[:10]  # top 10
#         }, 200
#     # missions du client au quel un freelance a postulé

#     def get_missions_client_applied_by_freelance(client_id):
#         """
#         Récupère toutes les missions du client ET les candidatures reçues
#         """
#         try:
#             # Récupérer toutes les missions du client
#             missions = Mission.query.filter_by(client_id=client_id).all()
            
#             if not missions:
#                 return {"missions_with_applications": []}, 200
            
#             # Pour chaque mission, récupérer les candidatures
#             missions_with_apps = []
            
#             for mission in missions:
#                 # Récupérer les applications pour cette mission
#                 applications = Application.query.filter_by(mission_id=mission.id).all()
                
#                 mission_data = mission.to_dict()
#                 mission_data['applications'] = [
#                     {
#                         'id': app.id,
#                         'freelance_id': app.freelance_id,
#                         'freelance_name': app.freelancer.name if app.freelancer else 'Unknown',
#                         'proposal': app.proposal,
#                         'proposed_budget': app.proposed_budget,
#                         'status': app.status,
#                         'created_at': app.created_at.isoformat() if app.created_at else None
#                     }
#                     for app in applications
#                 ]
#                 mission_data['applications_count'] = len(applications)
                
#                 missions_with_apps.append(mission_data)
            
#             return {
#                 "missions_with_applications": missions_with_apps,
#                 "total_missions": len(missions_with_apps),
#                 "total_applications": sum(len(m['applications']) for m in missions_with_apps)
#             }, 200
            
#         except Exception as e:
#             return {"message": f"Error: {str(e)}"}, 500

#         # Missions auxquelles le freelance a postulé

#     def get_missions_freelance_applied_to(freelance_id):
#         """
#         Récupère toutes les missions auxquelles le freelance a postulé
#         """
#         try:
#             # Récupérer toutes les applications du freelance
#             applications = Application.query.filter_by(freelance_id=freelance_id).all()
            
#             if not applications:
#                 return {"missions_applied": []}, 200
            
#             # Pour chaque application, récupérer les détails de la mission
#             missions_applied = []
            
#             for app in applications:
#                 mission = Mission.query.get(app.mission_id)
                
#                 if mission:
#                     mission_data = mission.to_dict()
#                     mission_data['application'] = {
#                         'id': app.id,
#                         'proposal': app.proposal,
#                         'proposed_budget': app.proposed_budget,
#                         'status': app.status,
#                         'created_at': app.created_at.isoformat() if app.created_at else None
#                     }
#                     mission_data['client_name'] = mission.client.name if mission.client else 'Unknown'
#                     mission_data['client_email'] = mission.client.email if mission.client else 'Unknown'
                    
#                     missions_applied.append(mission_data)
            
#             return {
#                 "missions_applied": missions_applied,
#                 "total_applications": len(missions_applied)
#             }, 200
            
#         except Exception as e:
#             return {"message": f"Error: {str(e)}"}, 500

#         # Récupérer les candidatures pour une mission spécifique
#     def get_mission_applications(mission_id):
#         """
#         Récupère toutes les candidatures pour une mission
#         """
#         try:
#             applications = Application.query.filter_by(mission_id=mission_id).all()
            
#             if not applications:
#                 return {"applications": []}, 200
            
#             applications_data = [
#                 {
#                     'id': app.id,
#                     'freelance_id': app.freelance_id,
#                     'freelance_name': app.freelancer.name if app.freelancer else 'Unknown',
#                     'freelance_email': app.freelancer.email if app.freelancer else 'Unknown',
#                     'proposal': app.proposal,
#                     'proposed_budget': app.proposed_budget,
#                     'status': app.status,
#                     'created_at': app.created_at.isoformat() if app.created_at else None,
#                     'freelancer_rating': app.freelancer.rating if app.freelancer else None,
#                     'freelancer_reviews_count': app.freelancer.reviews_count if app.freelancer else 0
#                 }
#                 for app in applications
#             ]
            
#             return {
#                 "applications": applications_data,
#                 "total_applications": len(applications_data)
#             }, 200
            
#         except Exception as e:
#             return {"message": f"Error: {str(e)}"}, 500

                

