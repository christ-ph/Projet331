from flask import request, jsonify
from models.models import * 

class UserController:

    def register_user(self, data):
        # vérifier si l'email existe déjà
        if User.query.filter_by(email=data['email']).first():
            return {"message": "Email already exists"}, 400
        
        new_user = User(email=data['email'], role=data.get('role', 'FREELANCE'))

        # sécurisation du password
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()
        
        # Créer un profil vide automatiquement
        profile_response = self.set_user_profile(new_user.id, {})
        
        return {"message": "User registered", "user_id": new_user.id, "user": new_user.to_dict()}, 201


    def set_user_profile(self, user_id, data):
        print(f"=== SET USER PROFILE DEBUG ===")
        print(f"User ID: {user_id}")
        print(f"Data received: {data}")
        
        user = User.query.get(user_id)
        if not user:
            print("User not found")
            return {"message": "User not found"}, 404
        
        print(f"User found - ID: {user.id}, Email: {user.email}, Role: {user.role}")
        
        try:
            if user.role == UserRole.FREELANCE:
                # Vérifier si le profil existe déjà
                existing_profile = FreelanceProfile.query.filter_by(user_id=user.id).first()
                
                if existing_profile:
                    print("Updating existing freelance profile")
                    # Mettre à jour le profil existant
                    existing_profile.first_name = data.get('first_name', existing_profile.first_name)
                    existing_profile.last_name = data.get('last_name', existing_profile.last_name)
                    existing_profile.title = data.get('title', existing_profile.title)
                    existing_profile.description = data.get('description', existing_profile.description)
                    existing_profile.hourly_rate = data.get('hourly_rate', existing_profile.hourly_rate)
                    existing_profile.availability = data.get('availability', existing_profile.availability)
                    existing_profile.skills = data.get('skills', existing_profile.skills)
                    
                    profile = existing_profile
                    action = "updated"
                else:
                    print("Creating new freelance profile")
                    # Créer un nouveau profil
                    profile = FreelanceProfile(
                        user_id=user.id,
                        first_name=data.get('first_name', ''),
                        last_name=data.get('last_name', ''),
                        title=data.get('title', ''),
                        description=data.get('description', ''),
                        skills=data.get('skills', []),
                        hourly_rate=data.get('hourly_rate', 0),
                        availability=data.get('availability', Availability.AVAILABLE)
                    )
                    db.session.add(profile)
                    action = "created"
                    
            elif user.role == UserRole.CLIENT:
                # Vérifier si le profil existe déjà
                existing_profile = ClientProfile.query.filter_by(user_id=user.id).first()
                
                if existing_profile:
                    print("Updating existing client profile")
                    # Mettre à jour le profil existant
                    existing_profile.company_name = data.get('company_name', existing_profile.company_name)
                    existing_profile.description = data.get('description', existing_profile.description)
                    
                    profile = existing_profile
                    action = "updated"
                else:
                    print("Creating new client profile")
                    # Créer un nouveau profil
                    profile = ClientProfile(
                        user_id=user.id,
                        company_name=data.get('company_name', ''),
                        description=data.get('description', '')
                    )
                    db.session.add(profile)
                    action = "created"
            else:
                return {"message": "Invalid role"}, 400

            db.session.commit()
            
            print(f"Profile {action} successfully - ID: {profile.id}")
            print(f"Profile details: {profile}")
            
            # Préparer la réponse en convertissant les enums en strings
            profile_response = {
                "first_name": getattr(profile, 'first_name', ''),
                "last_name": getattr(profile, 'last_name', ''),
                "title": getattr(profile, 'title', ''),
                "description": getattr(profile, 'description', ''),
                "company_name": getattr(profile, 'company_name', ''),
                "hourly_rate": getattr(profile, 'hourly_rate', 0),
                "skills": getattr(profile, 'skills', [])
            }
            
            # Gérer l'availability qui peut être un enum
            availability_value = getattr(profile, 'availability', 'AVAILABLE')
            if hasattr(availability_value, 'value'):
                profile_response["availability"] = availability_value.value
            else:
                profile_response["availability"] = str(availability_value)
            
            return {
                "message": f"Profile {action}", 
                "profile_id": profile.id,
                "action": action,
                "profile": profile_response
            }, 200 if action == "updated" else 201
            
        except Exception as e:
            db.session.rollback()
            print(f"Error processing profile: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"message": f"Error processing profile: {str(e)}"}, 500
    

    # def set_user_profile(self, user_id, data):
    #     user = User.query.get(user_id)
    #     print(user.role)
    #     if not user:
    #         return {"message": "User not found"}, 404
        
    #     # vérifier si le profile existe déjà 
    #     if user.role == UserRole.FREELANCE and user.freelance_profile:
    #         return {"message": "Freelance profile already exists"}, 400
    #     if user.role == "CLIENT" and user.client_profile:
    #         return {"message": "Client profile already exists"}, 400

    #     if user.role == UserRole.FREELANCE:
    #         # Créer un profil freelance avec des valeurs par défaut
    #         profile = FreelanceProfile(
    #             user_id=user.id,
    #             first_name=data.get('first_name'),  # sera None par défaut
    #             last_name=data.get('last_name'),    # sera None par défaut
    #             title=data.get('title'),            # sera None par défaut
    #             description=data.get('description'), # sera None par défaut
    #             skills=data.get('skills', []),      # liste vide par défaut
    #             hourly_rate=data.get('hourly_rate'), # sera None par défaut
    #             availability=data.get('availability', Availability.AVAILABLE)
    #         )
    #         print(profile)
    #     elif user.role == UserRole.CLIENT:
    #         # Créer un profil client avec des valeurs par défaut
    #         profile = ClientProfile(
    #             user_id=user.id,
    #             company_name=data.get('company_name'), # sera None par défaut
    #             description=data.get('description')    # sera None par défaut
    #         )
    #     else:
    #         return {"message": "Invalid role"}, 400

    #     db.session.add(profile)
    #     db.session.commit()
    #     return {"message": "Profile created", "profile_id": profile.id}, 201