
from flask_restful import Resource, reqparse
from flask import request
from controllers.Module2_Client_Management.mission_controller import MissionController
from models.models import Mission  # FIX: Import manquant

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


class MissionLastOffersResource(Resource):
    def get(self):
        # Pas besoin d'être authentifié
        return controller.get_last_offres()


class MissionFreelanceMissionsResource(Resource):
    def get(self, freelance_id):
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401

        if authenticated_id != freelance_id:
            return {"message": "Access denied"}, 403

        return controller.get_freelance_missions(freelance_id)


class MissionRecommendedFreelancersResource(Resource):
    def get(self, mission_id):
        client_id = get_authenticated_user_id()
        if not client_id:
            return {"message": "Authentication required"}, 401

        return controller.get_recommended_freelancers(mission_id)


class MissionClientAppliedByFreelanceResource(Resource):
    def get(self, client_id):
        """
        Récupère les missions du client avec les candidatures reçues
        """
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        
        if authenticated_id != client_id:
            return {"message": "Access denied"}, 403
        
        return controller.get_missions_client_applied_by_freelance(client_id)


class MissionFreelanceAppliedResource(Resource):
    def get(self, freelance_id):
        """
        Récupère les missions auxquelles le freelance a postulé
        """
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        
        if authenticated_id != freelance_id:
            return {"message": "Access denied"}, 403
        
        return controller.get_missions_freelance_applied_to(freelance_id)

class MissionApplicationsResource(Resource):
    """
    Récupère la liste des candidatures pour une mission spécifique.
    Accessible seulement au client propriétaire de la mission.
    """
    def get(self, mission_id):
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        
        # Le MissionController contient déjà la logique de vérification d'autorisation
        # dans la fonction get_mission_applications, mais on peut la laisser ici pour plus de clarté
        mission = Mission.query.get(mission_id)
        if not mission:
            return {"message": "Mission not found"}, 404
        
        # Vérifier que c'est le client propriétaire
        if authenticated_id != mission.client_id:
            return {"message": "Access denied. Only the mission owner can view applications."}, 403
        
        return controller.get_mission_applications(mission_id)


class FreelanceActiveMissionsResource(Resource):
    """
    Récupère les missions actives (ACCEPTED) pour le freelance authentifié.
    L'ID du freelance est déduit de l'utilisateur authentifié pour plus de sécurité.
    """
    def get(self):
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        
        # L'ID du freelance est l'ID authentifié. On utilise l'ID du chemin d'accès
        # dans l'URL seulement si la route le nécessite, sinon on utilise l'ID authentifié.
        # Si vous utilisez un paramètre freelance_id dans l'URL, vous devez le comparer ici:
        # if authenticated_id != freelance_id:
        #     return {"message": "Access denied"}, 403
        
        # On passe directement l'ID de l'utilisateur authentifié au controller
        return controller.get_active_missions(authenticated_id)


class ApplicationStatusUpdateResource(Resource):
    """
    Met à jour le statut d'une candidature (Accepté/Refusé).
    Accessible seulement au client propriétaire de la mission associée.
    """
    def put(self, application_id):
        authenticated_id = get_authenticated_user_id()
        if not authenticated_id:
            return {"message": "Authentication required"}, 401
        
        parser = reqparse.RequestParser()
        parser.add_argument('status', 
                            type=str, 
                            required=True, 
                            help='Status (ACCEPTED or REJECTED) is required', 
                            location='json') # Assurez-vous d'utiliser 'json' ou 'form' selon l'API
        args = parser.parse_args()

        # Le controller se chargera de vérifier si authenticated_id est bien le client propriétaire
        return controller.update_application_status(application_id, authenticated_id, args['status'])
class MissionDetailedResource(Resource):
    def get(self, mission_id):
        """
        GET /api/missions/<int:mission_id>/detailed
        Vue détaillée avec infos selon l'utilisateur connecté
        """
        user_id = get_authenticated_user_id()  # Votre fonction d'authentification
        return controller.get_mission_detailed_view(mission_id, user_id)
class MissionCompleteOrCancelResource(Resource):
    
    def put(self, mission_id):
        client_id = get_authenticated_user_id() 
        
        if not client_id:
            return {"message": "Authentification requise."}, 401

        # 🔍 DEBUG COMPLET
        print("=" * 50)
        print("DEBUG: Début du traitement PUT /api/missions/{mission_id}/status")
        print(f"DEBUG: mission_id: {mission_id}")
        print(f"DEBUG: client_id: {client_id}")
        print(f"DEBUG: Headers: {dict(request.headers)}")
        print(f"DEBUG: Content-Type: {request.headers.get('Content-Type')}")

        try:
            # 1. Vérifier le Content-Type
            content_type = request.headers.get('Content-Type', '')
            if not content_type.startswith('application/json'):
                print("DEBUG: ❌ Mauvais Content-Type")
                return {"message": "Content-Type doit être application/json"}, 400
            
            # 2. Lire les données brutes
            raw_data = request.get_data(as_text=True)
            print(f"DEBUG: Raw data reçu: '{raw_data}'")
            print(f"DEBUG: Longueur des données: {len(raw_data)}")
            
            if not raw_data or raw_data.strip() == '':
                print("DEBUG: ❌ Données brutes vides")
                return {"message": "Corps JSON vide."}, 400
            
            # 3. Parser le JSON
            import json
            try:
                json_data = json.loads(raw_data)
                print(f"DEBUG: ✅ JSON parsé avec succès: {json_data}")
                print(f"DEBUG: Type des données parsées: {type(json_data)}")
            except json.JSONDecodeError as e:
                print(f"DEBUG: ❌ Erreur JSON: {e}")
                return {"message": f"JSON invalide: {str(e)}"}, 400
            
            # 4. Vérifier que c'est bien un dictionnaire
            if not isinstance(json_data, dict):
                print(f"DEBUG: ❌ Type invalide: {type(json_data)}, valeur: {json_data}")
                return {"message": "Le corps doit être un objet JSON (dictionnaire)"}, 400
            
            # 5. Vérifier le champ requis
            if 'status_cible' not in json_data:
                print(f"DEBUG: ❌ Champ 'status_cible' manquant. Champs disponibles: {list(json_data.keys())}")
                return {"message": "Le champ 'status_cible' est requis."}, 400
                
            status_cible = json_data['status_cible']
            print(f"DEBUG: status_cible trouvé: '{status_cible}' (type: {type(status_cible)})")
            
            if not isinstance(status_cible, str) or not status_cible.strip():
                print(f"DEBUG: ❌ status_cible invalide")
                return {"message": "Le champ 'status_cible' doit être une chaîne non vide."}, 400
            
            # 6. Préparer les données pour le contrôleur
            data = {'status_cible': status_cible.strip().upper()}
            print(f"DEBUG: ✅ Données préparées pour contrôleur: {data}")
            
        except Exception as e:
            print(f"DEBUG: ❌ Erreur critique lors du parsing: {e}")
            import traceback
            traceback.print_exc()
            return {"message": "Erreur de traitement de la requête."}, 400
        
        # 7. Appel du contrôleur
        print(f"DEBUG: 📞 Appel du contrôleur avec mission_id={mission_id}, client_id={client_id}")
        try:
            response, status_code = controller.complete_or_cancel_mission(
                mission_id=mission_id, 
                client_id=client_id, 
                data=data
            )
            print(f"DEBUG: ✅ Réponse du contrôleur: {status_code}")
            return response, status_code
        except Exception as e:
            print(f"DEBUG: ❌ Erreur dans le contrôleur: {e}")
            import traceback
            traceback.print_exc()
            return {"message": "Erreur interne du serveur"}, 500



# from flask_restful import Resource, reqparse
# from flask import request
# from controllers.Module2_Client_Management.mission_controller import MissionController

# controller = MissionController()

# # --- Authentification simplifiée ---
# def get_authenticated_user_id():
#     """Récupère l'ID utilisateur depuis le header 'User-ID'."""
#     user_id = request.headers.get('User-ID')
#     try:
#         return int(user_id) if user_id else None
#     except ValueError:
#         return None

# # --- Resources ---
# class MissionListResource(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('skills', type=str, location='args')
#         parser.add_argument('min_budget', type=float, location='args')
#         parser.add_argument('max_budget', type=float, location='args')
#         parser.add_argument('status', type=str, location='args', default='PUBLISHED')
#         args = parser.parse_args()

#         filters = {k: v for k, v in args.items() if v is not None}
#         return controller.get_all_missions(filters=filters)

#     def post(self):
#         client_id = get_authenticated_user_id()
#         if not client_id:
#             return {"message": "Authentication required"}, 401

#         parser = reqparse.RequestParser()
#         parser.add_argument('title', type=str, required=True, help='Title is required')
#         parser.add_argument('description', type=str, required=True, help='Description is required')
#         parser.add_argument('budget', type=float, required=True, help='Budget is required')
#         parser.add_argument('budget_type', type=str, required=True, help='Budget type is required')
#         parser.add_argument('deadline', type=str, required=True, help='Deadline is required')
#         parser.add_argument('required_skills', type=list, location='json', default=[])
#         parser.add_argument('status', type=str, default='DRAFT')
#         args = parser.parse_args()

#         return controller.create_mission(client_id, args)


# class MissionResource(Resource):
#     def get(self, mission_id):
#         return controller.get_mission_by_id(mission_id)

#     def put(self, mission_id):
#         client_id = get_authenticated_user_id()
#         if not client_id:
#             return {"message": "Authentication required"}, 401

#         parser = reqparse.RequestParser()
#         parser.add_argument('title', type=str)
#         parser.add_argument('description', type=str)
#         parser.add_argument('budget', type=float)
#         parser.add_argument('budget_type', type=str)
#         parser.add_argument('deadline', type=str)
#         parser.add_argument('required_skills', type=list, location='json')
#         parser.add_argument('status', type=str)
#         args = parser.parse_args()

#         update_data = {k: v for k, v in args.items() if v is not None}
#         return controller.update_mission(mission_id, client_id, update_data)

#     def delete(self, mission_id):
#         client_id = get_authenticated_user_id()
#         if not client_id:
#             return {"message": "Authentication required"}, 401

#         return controller.delete_mission(mission_id, client_id)


# class ApplicationResource(Resource):
#     def post(self, mission_id):
#         freelance_id = get_authenticated_user_id()
#         if not freelance_id:
#             return {"message": "Authentication required"}, 401

#         parser = reqparse.RequestParser()
#         parser.add_argument('proposal', type=str, required=True, help='Proposal is required')
#         parser.add_argument('proposed_budget', type=float)
#         parser.add_argument('delivery_time', type=str)
#         args = parser.parse_args()

#         return controller.apply_to_mission(mission_id, freelance_id, args)


# class UserMissionsResource(Resource):
#     def get(self, user_id):
#         authenticated_id = get_authenticated_user_id()
#         if not authenticated_id:
#             return {"message": "Authentication required"}, 401
#         if authenticated_id != user_id:
#             return {"message": "Access denied"}, 403

#         return controller.get_user_missions(user_id)


# class UserApplicationsResource(Resource):
#     def get(self, user_id):
#         authenticated_id = get_authenticated_user_id()
#         if not authenticated_id:
#             return {"message": "Authentication required"}, 401
#         if authenticated_id != user_id:
#             return {"message": "Access denied"}, 403

#         return controller.get_user_applications(user_id)


# class MissionLastOffersResource(Resource):
#     def get(self):
#         # Pas besoin d’être authentifié
#         return controller.get_last_offres()

# class MissionFreelanceMissionsResource(Resource):
#     def get(self, freelance_id):
#         authenticated_id = get_authenticated_user_id()
#         if not authenticated_id:
#             return {"message": "Authentication required"}, 401

#         if authenticated_id != freelance_id:
#             return {"message": "Access denied"}, 403

#         return controller.get_freelance_missions(freelance_id)
    
#     # recommander des freelances pour une mission donnée 
# class MissionRecommendedFreelancersResource(Resource):
#     def get(self, mission_id):
#         client_id = get_authenticated_user_id()
#         if not client_id:
#             return {"message": "Authentication required"}, 401

#         return controller.get_recommended_freelancers(mission_id)
# class MissionClientAppliedByFreelanceResource(Resource):
#     def get(self, client_id):
#         """
#         Récupère les missions du client avec les candidatures reçues
#         """
#         authenticated_id = get_authenticated_user_id()
#         if not authenticated_id:
#             return {"message": "Authentication required"}, 401
        
#         if authenticated_id != client_id:
#             return {"message": "Access denied"}, 403
        
#         return controller.get_missions_client_applied_by_freelance(client_id)
# class MissionFreelanceAppliedResource(Resource):
#     def get(self, freelance_id):
#         """
#         Récupère les missions auxquelles le freelance a postulé
#         """
#         authenticated_id = get_authenticated_user_id()
#         if not authenticated_id:
#             return {"message": "Authentication required"}, 401
        
#         if authenticated_id != freelance_id:
#             return {"message": "Access denied"}, 403
        
#         return controller.get_missions_freelance_applied_to(freelance_id)

# class MissionApplicationsSpecifiquesResource(Resource):
#     def get(self, mission_id):
#         """
#         Récupère les candidatures pour une mission donnée
#         Accessible seulement au client propriétaire de la mission
#         """
#         authenticated_id = get_authenticated_user_id()
#         if not authenticated_id:
#             return {"message": "Authentication required"}, 401
        
#         mission = Mission.query.get(mission_id)
#         if not mission:
#             return {"message": "Mission not found"}, 404
        
#         # Vérifier que c'est le client propriétaire
#         if authenticated_id != mission.client_id:
#             return {"message": "Access denied"}, 403
        
#         return controller.get_mission_applications(mission_id)