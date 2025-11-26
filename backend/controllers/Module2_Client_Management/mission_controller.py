from datetime import datetime
from sqlalchemy.orm import joinedload
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
                    "budget": mission.budget,  # 🔧 AJOUT: Budget de la mission
                    "created_at": mission.created_at.isoformat() if mission.created_at else None,
                    "applications": []
                }

                for app in applications:
                    # --- CORRECTION DE L'ACCÈS AU PROFIL FREELANCE ---
                    freelance_user = app.freelance # Ceci est l'objet User
                    freelance_name = "Unknown"
                    
                    if freelance_user and freelance_user.freelance_profile:
                        profile = freelance_user.freelance_profile
                        # Utilise le prénom et nom du profil
                        freelance_name = f"{profile.first_name} {profile.last_name}"
                    
                    # 🔧 CORRECTION DU BUDGET : Utiliser le budget de la mission si le freelance propose 0
                    proposed_budget = app.proposed_budget
                    if proposed_budget is None or proposed_budget == 0:
                        proposed_budget = mission.budget  # Utiliser le budget de la mission
                    
                    mission_data["applications"].append({
                        "id": app.id,
                        "freelance_id": app.freelance_id,
                        "freelance_name": freelance_name,
                        "proposal": app.proposal,
                        "proposed_budget": proposed_budget,  # 🔧 MAINTENANT AVEC BUDGET DE LA MISSION SI 0
                        "original_proposed_budget": app.proposed_budget,  # 🔧 OPTIONNEL: Garder la valeur originale
                        "status": app.status.value if app.status else None, 
                        "created_at": app.created_at.isoformat() if app.created_at else None
                    })
                    # ----------------------------------------------------

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
 # -------------------------------------------------------
    # 🔹 APPLICATIONS FOR A MISSION
    # -------------------------------------------------------
    def get_mission_applications(self, mission_id):
        try:
            applications = Application.query.filter_by(mission_id=mission_id).all()
            if not applications:
                return {"applications": []}, 200

            applications_data = []
            for app in applications:
                # --- CORRECTION DE L'ACCÈS AU PROFIL FREELANCE ---
                freelance_user = app.freelance # Ceci est l'objet User
                freelance_profile = freelance_user.freelance_profile if freelance_user else None
                
                freelance_name = 'Unknown'
                freelance_email = 'Unknown'
                freelancer_rating = None
                freelancer_reviews_count = 0
                
                if freelance_user:
                    freelance_email = freelance_user.email
                    
                    if freelance_profile:
                        # Assurez-vous que les champs 'rating' et 'reviews_count' existent sur FreelanceProfile
                        # Si ce n'est pas le cas, vous devrez les ajouter au modèle FreelanceProfile.
                        freelance_name = f"{freelance_profile.first_name} {freelance_profile.last_name}"
                        # Ces lignes peuvent encore causer une erreur si ces champs n'existent pas sur FreelanceProfile
                        # Assurez-vous d'avoir les attributs 'rating' et 'reviews_count' sur le modèle FreelanceProfile !
                        # freelancer_rating = getattr(freelance_profile, 'rating', None) 
                        # freelancer_reviews_count = getattr(freelance_profile, 'reviews_count', 0)
                        
                        # --- REMPLACEMENT TEMPORAIRE (à adapter si vous n'avez pas ces champs) ---
                        # Puisque 'rating' et 'reviews_count' ne sont pas dans le modèle FreelanceProfile que vous m'avez donné,
                        # je les laisse temporairement à None/0 pour éviter une erreur d'attribut.
                        # Vous DEVEZ les ajouter au modèle FreelanceProfile si vous voulez les afficher.
                        pass 
                        # --------------------------------------------------------------------------

                applications_data.append({
                    'id': app.id,
                    'freelance_id': app.freelance_id,
                    'freelance_name': freelance_name,        # CORRIGÉ
                    'freelance_email': freelance_email,      # CORRIGÉ
                    'proposal': app.proposal,
                    'proposed_budget': app.proposed_budget,
                    'status': app.status.value if app.status else None, # Conversion de l'Enum
                    'created_at': app.created_at.isoformat() if app.created_at else None,
                    'freelancer_rating': freelancer_rating,              # CORRIGÉ (via profil)
                    'freelancer_reviews_count': freelancer_reviews_count # CORRIGÉ (via profil)
                })
            # ---------------------------------------------------

            return {
                "applications": applications_data,
                "total_applications": len(applications_data)
            }, 200

        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 500
        

#mission avce detail
    def get_mission_detailed_view(self, mission_id, user_id=None):
        """
        Vue détaillée avec informations supplémentaires selon l'utilisateur
        """
        try:
            # Chargement optimisé avec jointures
            mission = Mission.query.options(
                joinedload(Mission.client).joinedload(User.client_profile)
            ).get(mission_id)
            
            if not mission:
                return {"message": "Mission non trouvée"}, 404
            
            # Données de base de la mission
            mission_data = {
                "id": mission.id,
                "title": mission.title,
                "description": mission.description,
                "budget": mission.budget,
                "budget_type": mission.budget_type,
                "deadline": mission.deadline.isoformat() if mission.deadline else None,
                "status": mission.status.value,
                "required_skills": mission.required_skills or [],
                "created_at": mission.created_at.isoformat(),
                "updated_at": mission.updated_at.isoformat() if mission.updated_at else None,
            }
            
            # Données client complètes
            client_data = None
            if mission.client:
                client_data = {
                    "id": mission.client.id,
                    "email": mission.client.email,
                    "role": mission.client.role.value,
                    "created_at": mission.client.created_at.isoformat() if mission.client.created_at else None,
                }
                
                if mission.client.client_profile:
                    client_data["profile"] = {
                        "company_name": mission.client.client_profile.company_name,
                        "description": mission.client.client_profile.description
                    }
            
            # Construction de la réponse de base
            response_data = {
                "mission": mission_data,
                "client": client_data
            }
            
            # Informations supplémentaires selon l'utilisateur
            if user_id:
                # Si l'utilisateur est le client propriétaire
                if mission.client_id == user_id:
                    response_data["is_owner"] = True
                    response_data["applications_count"] = len(mission.applications)
                
                # Si l'utilisateur est un freelance, vérifier s'il a postulé
                else:
                    application = Application.query.filter_by(
                        mission_id=mission_id,
                        freelance_id=user_id
                    ).first()
                    
                    response_data["has_applied"] = application is not None
                    if application:
                        response_data["my_application"] = {
                            "id": application.id,
                            "status": application.status.value,
                            "created_at": application.created_at.isoformat()
                        }
            
            return response_data, 200
            
        except Exception as e:
            return {"message": f"Erreur lors de la récupération de la mission: {str(e)}"}, 500

    def get_missions_freelance_applied_to(self, freelance_id):
        """
        Récupère toutes les missions auxquelles le freelance a postulé, 
        en sécurisant l'accès aux données du client via le profil.
        """

        try:
            # Récupérer toutes les applications du freelance
            applications = Application.query.filter_by(freelance_id=freelance_id).all()
            
            if not applications:
                return {"missions_applied": []}, 200
            
            # Pour chaque application, récupérer les détails de la mission
            missions_applied = []
            
            for app in applications:
                mission = Mission.query.get(app.mission_id)
                
                if mission:
                    mission_data = mission.to_dict()
                    
                    # Données de l'application
                    mission_data['application'] = {
                        'id': app.id,
                        'proposal': app.proposal,
                        'proposed_budget': app.proposed_budget,
                        'status': app.status.value if app.status else None, # Sécuriser l'accès à l'Enum
                        'created_at': app.created_at.isoformat() if app.created_at else None
                    }
                    
                    # --- CORRECTION DE L'ACCÈS AU CLIENT ---
                    client_user = mission.client # Ceci est l'objet User
                    
                    if client_user:
                        mission_data['client_email'] = client_user.email
                        client_profile = client_user.client_profile

                        if client_profile:
                            # Utilise le nom de l'entreprise du ClientProfile
                            mission_data['client_name'] = client_profile.company_name
                        else:
                            # Repli si l'utilisateur client n'a pas encore de profil client (peu probable)
                            mission_data['client_name'] = client_user.email.split('@')[0]
                    else:
                        # Repli si la relation User est None (problème d'intégrité ou ORM)
                        mission_data['client_name'] = 'Unknown'
                        mission_data['client_email'] = 'Unknown'
                    # ----------------------------------------
                    
                    missions_applied.append(mission_data)
            
            return {
                "missions_applied": missions_applied,
                "total_applications": len(missions_applied)
            }, 200
            
        except Exception as e:
            # Assurez-vous d'avoir accès à Mission et Application dans la portée de votre fichier
            # sinon, déplacez l'importation au début du fichier
            return {"message": f"Error: {str(e)}"}, 500
        

    # -------------------------------------------------------
    # 🔹 CLIENT: UPDATE APPLICATION STATUS (NEW)
    # Rôle: Le client accepte/refuse une candidature.
    # Conséquence: Si ACCEPTED, Mission.status passe à IN_PROGRESS
    # -------------------------------------------------------
    def update_application_status(self, application_id: int, client_id: int, new_status: str):
        """
        Permet au client d'accepter ou de refuser une candidature.
        Si la candidature est acceptée, la mission passe à IN_PROGRESS et les autres candidatures sont refusées.
        """
        try:
            # 1. Valider le nouveau statut
            try:
                # Convertir le statut en majuscules pour l'Enum
                target_status = ApplicationStatus(new_status.upper())
            except ValueError:
                return {"message": "Statut invalide. Utilisez ACCEPTED ou REJECTED."}, 400

            # 2. Trouver la candidature
            application = db.session.get(Application, application_id)
            if not application:
                return {"message": "Candidature non trouvée."}, 404
            
            # 3. Trouver la mission et vérifier les autorisations
            mission = application.mission # Accès via la relation ORM si elle existe
            if not mission:
                # Si la relation n'existe pas, on cherche par ID
                mission = Mission.query.get(application.mission_id)
            
            if not mission:
                return {"message": "Mission associée non trouvée."}, 404
            
            # Vérification d'autorisation: Le client doit être le propriétaire de la mission
            if mission.client_id != client_id:
                return {"message": "Accès refusé. Vous n'êtes pas le client propriétaire de cette mission."}, 403
            
            
            # --- LOGIQUE TRANSACTIONNELLE CRITIQUE ---
            
            # 4. Mettre à jour la candidature
            application.status = target_status
            
            
            if target_status == ApplicationStatus.ACCEPTED:
                
                # A. Changer le statut de la mission à 'IN_PROGRESS'
                mission.status = MissionStatus.IN_PROGRESS
                
                # B. Refuser automatiquement les autres candidatures en attente pour cette mission
                # Utilisation de la méthode de mise à jour groupée pour l'efficacité
                Application.query.filter(
                    Application.mission_id == mission.id,
                    Application.id != application_id,
                    Application.status == ApplicationStatus.PENDING
                ).update(
                    {'status': ApplicationStatus.REJECTED}, 
                    synchronize_session=False
                )
                
                status_message = "Candidature acceptée. La mission est passée à IN_PROGRESS et les autres candidatures ont été refusées."
                
            elif target_status == ApplicationStatus.REJECTED:
                status_message = "Candidature refusée."
            
            # 5. Commit de toutes les modifications
            db.session.commit()
            
            return {
                "message": status_message,
                "application": application.to_dict(),
                "mission_status": mission.status.value
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Erreur serveur lors de la mise à jour: {str(e)}"}, 500


    # -------------------------------------------------------
    # 🔹 FREELANCE: GET ACTIVE MISSIONS (NEW)
    # Rôle: Récupérer les missions dont la candidature du freelance est ACCEPTED.
    # -------------------------------------------------------
    def get_active_missions(self, freelance_id: int):
        """
        Récupère les missions dont la candidature du freelance a été ACCEPTED 
        (et qui sont donc en cours - IN_PROGRESS).
        """
        try:
            # 1. Trouver les applications ACCEPTED par ce freelance
            applications = Application.query.filter_by(
                freelance_id=freelance_id, 
                status=ApplicationStatus.ACCEPTED
            ).all()
            
            if not applications:
                return {"active_missions": []}, 200

            active_missions_data = []

            for app in applications:
                mission = app.mission 
                
                # 2. Vérifier le statut de la Mission (sécurité)
                if mission and mission.status == MissionStatus.IN_PROGRESS:
                    
                    # Récupération sécurisée des infos client
                    client_name = 'Unknown'
                    client_email = 'Unknown'
                    if mission.client:
                        client_email = mission.client.email
                        if mission.client.client_profile:
                            client_name = mission.client.client_profile.company_name

                    # Données de la mission
                    mission_data = {
                        "id": mission.id,
                        "title": mission.title,
                        "description": mission.description,
                        "budget": mission.budget,
                        "budget_type": mission.budget_type,
                        "deadline": mission.deadline.isoformat() if mission.deadline else None,
                        "status": mission.status.value,
                        "required_skills": mission.required_skills,
                        "created_at": mission.created_at.isoformat() if mission.created_at else None,
                        "client_id": mission.client_id,
                        
                        # Infos client et application
                        'application_status': app.status.value,
                        'application_id': app.id,
                        'client_name': client_name,
                        'client_email': client_email,
                        'proposed_budget': app.proposed_budget,
                        'delivery_time': app.delivery_time
                    }

                    active_missions_data.append(mission_data)

            return {
                "active_missions": active_missions_data,
                "total_active": len(active_missions_data)
            }, 200

        except Exception as e:
            return {"message": f"Erreur lors de la récupération des missions actives: {str(e)}"}, 500
# -------------------------------------------------------
    # 🔹 TERMINER OU ANNULER UNE MISSION (Rôle Client)
    # -------------------------------------------------------
    def complete_or_cancel_mission(self, mission_id: int, client_id: int, data: dict):
        """
        Permet au client de changer le statut de la mission à COMPLETE ou CANCELLED.
        """
        
        status_cible_str = data.get('status_cible', '').upper()
        
        print(f"🔍 DEBUG CONTROLEUR:")
        print(f"   mission_id: {mission_id}")
        print(f"   client_id: {client_id}")
        print(f"   data reçu: {data}")
        print(f"   status_cible_str: '{status_cible_str}'")
        
        # 🔧 CORRECTION: Utiliser les valeurs EXACTES de votre enum
        VALID_STATUSES = ['COMPLETE', 'CANCELLED']  # COMPLETE sans 'D' !
        
        print(f"   Statuts valides: {VALID_STATUSES}")
        
        if status_cible_str not in VALID_STATUSES:
            print(f"   ❌ Statut '{status_cible_str}' non valide")
            return {
                "message": f"Statut cible non valide. Utilisez: 'COMPLETE' ou 'CANCELLED'"
            }, 400
        
        try:
            # 🔧 CORRECTION: Votre enum utilise COMPLETE (sans D)
            target_status = MissionStatus(status_cible_str)
            print(f"   ✅ Conversion réussie: {target_status} (valeur: {target_status.value})")
            
        except ValueError as e:
            print(f"   ❌ Erreur de conversion: {e}")
            return {
                "message": f"Erreur de conversion. Statut '{status_cible_str}' non reconnu. Utilisez 'COMPLETE' ou 'CANCELLED'."
            }, 400

        try:
            # Récupérer la mission
            mission = Mission.query.get(mission_id)
            if not mission:
                return {"message": "Mission non trouvée."}, 404

            # Vérification des autorisations
            if mission.client_id != client_id:
                return {"message": "Accès refusé. Vous n'êtes pas le client propriétaire de cette mission."}, 403
            
            current_status = mission.status.value
            print(f"   📊 Statut actuel de la mission: {current_status}")
            
            # 🔧 CORRECTION: Vérifications avec les bonnes valeurs
            if target_status.value == 'COMPLETE':  # COMPLETE sans D
                if current_status != 'IN_PROGRESS': 
                    return {
                        "message": f"Impossible de marquer la mission comme COMPLETE. Statut actuel: '{current_status}'. La mission doit être 'IN_PROGRESS'."
                    }, 400
            
            elif target_status.value == 'CANCELLED':
                if current_status == 'COMPLETE':  # COMPLETE sans D
                    return {"message": "Impossible d'annuler une mission déjà COMPLETE."}, 400
            
            # Mettre à jour le statut
            mission.status = target_status
            db.session.commit()
            
            print(f"   ✅ Mission {mission_id} mise à jour vers '{target_status.value}'")
            
            return {
                "message": f"Mission {mission_id} mise à jour au statut '{target_status.value}' avec succès.",
                "mission": mission.to_dict()
            }, 200

        except Exception as e:
            db.session.rollback()
            print(f"   ❌ Erreur base de données: {e}")
            return {"message": f"Erreur interne lors de la mise à jour du statut: {str(e)}"}, 500









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

                

