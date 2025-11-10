from flask import request, jsonify
from models.models import * 

class FreelanceController:

    def get_all_profiles(self):
        profiles = FreelanceProfile.query.all()
        return [p.to_dict() for p in profiles], 200

    def get_profile_by_id(self, profile_id):
        profile = FreelanceProfile.query.get(profile_id)
        if not profile:
            return {"message": "Profile not found"}, 404
        return profile.to_dict(include_portfolio=True), 200

    def create_profile(self, data):
        profile = FreelanceProfile(**data)
        db.session.add(profile)
        db.session.commit()
        return profile.to_dict(), 201

    def update_profile(self, user_id, data):
        try:
            print("=== update_profile called ===")
            print("user_id reçu :", user_id)
            print("data reçue :", data)

            user = User.query.get(user_id)
            print("user trouvé :", user)

            if not user:
                print("⚠️ Utilisateur non trouvé")
                return {"message": "User not found"}, 404

            # Déterminer quel profil mettre à jour selon le rôle (avec Enum)
            if user.role == UserRole.FREELANCE:
                profile = user.freelance_profile
                print("profil freelance :", profile)
                if not profile:
                    print("⚠️ Profil freelance non trouvé")
                    return {"message": "Freelance profile not found"}, 404
            elif user.role == UserRole.CLIENT:
                profile = user.client_profile
                print("profil client :", profile)
                if not profile:
                    print("⚠️ Profil client non trouvé")
                    return {"message": "Client profile not found"}, 404
            else:
                print("⚠️ Rôle utilisateur invalide :", user.role)
                return {"message": "Invalid user role"}, 400

            # Mettre à jour les champs autorisés
            allowed_fields = []
            if user.role == UserRole.FREELANCE:
                allowed_fields = ['first_name', 'last_name', 'title', 'description', 'skills', 'hourly_rate', 'availability']
            elif user.role == UserRole.CLIENT:
                allowed_fields = ['company_name', 'description']

            print("Champs autorisés :", allowed_fields)

            # Filtrer les champs autorisés et les mettre à jour
            updated_fields = []
            for key, value in data.items():
                if key in allowed_fields:
                    setattr(profile, key, value)
                    updated_fields.append(key)

            print("Champs mis à jour :", updated_fields)

            db.session.commit()
            print("✅ Profil mis à jour avec succès")

            return profile.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            print("❌ Exception levée :", str(e))
            return {"message": f"Error updating profile: {str(e)}"}, 500

    def delete_profile(self, profile_id):
        profile = FreelanceProfile.query.get(profile_id)
        if not profile:
            return {"message": "Profile not found"}, 404
        db.session.delete(profile)
        db.session.commit()
        return {"message": "Profile deleted"}, 200

    # ====== PORTFOLIO ======
    def get_portfolio_items(self, profile_id):
        """Récupère tous les projets du portfolio d’un profil freelance"""
        profile = FreelanceProfile.query.get(profile_id)
        if not profile:
            return {"message": "Freelance profile not found"}, 404
        items = PortfolioItem.query.filter_by(freelance_profile_id=profile_id).all()
        return [item.to_dict() for item in items], 200

    def get_portfolio_item(self, item_id):
        """Récupère un projet spécifique"""
        item = PortfolioItem.query.get(item_id)
        if not item:
            return {"message": "Portfolio item not found"}, 404
        return item.to_dict(), 200

    def add_portfolio_item(self, profile_id, data):
        """Ajoute un nouveau projet au portfolio"""
        profile = FreelanceProfile.query.get(profile_id)
        if not profile:
            return {"message": "Freelance profile not found"}, 404

        item = PortfolioItem(
            freelance_profile_id=profile_id,
            title=data.get("title"),
            description=data.get("description"),
            image_url=data.get("image_url"),
            project_url=data.get("project_url")
        )
        db.session.add(item)
        db.session.commit()
        return item.to_dict(), 201

    def update_portfolio_item(self, profile_id, item_id, data):
        """Met à jour un projet du portfolio d’un profil"""
        item = PortfolioItem.query.filter_by(id=item_id, profile_id=profile_id).first()
        if not item:
            return {"message": "Portfolio item not found"}, 404

        item.title = data.get("title", item.title)
        item.description = data.get("description", item.description)
        item.image_url = data.get("image_url", item.image_url)
        item.project_url = data.get("project_url", item.project_url)

        db.session.commit()
        return item.to_dict(), 200

    def remove_portfolio_item(self, item_id):
        """Supprime un projet du portfolio"""
        item = PortfolioItem.query.get(item_id)
        if not item:
            return {"message": "Portfolio item not found"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"message": "Portfolio item deleted"}, 200


    def get_profile_by_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        if user.role != "FREELANCE":
            return {"message": "This user is not a freelance"}, 400
        profile = user.freelance_profile
        if not profile:
            return {"message": "Freelance profile not found"}, 404
        return profile.to_dict(include_portfolio=True), 200

    def delete_profile_by_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        if user.role != "FREELANCE":
            return {"message": "This user is not a freelance"}, 400
        profile = user.freelance_profile
        if not profile:
            return {"message": "Freelance profile not found"}, 404
        db.session.delete(profile)
        db.session.commit()
        return {"message": "Freelance profile deleted"}, 200
