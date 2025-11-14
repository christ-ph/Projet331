# [file name]: app.py - VERSION CORRIGÉE COMPLÈTE
from dotenv import load_dotenv
import os
from flask import Flask
from models.models import db
from ressources.Module1_Register_User.freelance_ressource import *
from ressources.Module1_Register_User.user_ressource import *
from ressources.Module1_Register_User.ConnectionUserResource import *
from  ressources.Module2_Client_Managment.mission_ressource import *
from flask_restful import Api
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    # db.drop_all()  # ⚠️ Supprimez cette ligne après la première exécution
    db.create_all()
    print("✅ Tables créées avec succès!")

# Routes utilisateur
api.add_resource(RegisterUserResource, '/api/register')
api.add_resource(ConnectionUserResource, '/api/login')
api.add_resource(SetUserProfileResource, '/api/users/<int:user_id>/profile')

# Routes freelances
api.add_resource(FreelanceListResource, '/api/profiles')
api.add_resource(FreelanceResource, '/api/profiles/<int:user_id>')

# Routes Portfolio
api.add_resource(PortfolioListResource, '/api/profiles/<int:profile_id>/portfolio')
api.add_resource(PortfolioItemResource, '/api/profiles/<int:profile_id>/portfolio/<int:item_id>')

# Routes Missions - ✅ VERSION CORRIGÉE
api.add_resource(MissionListResource, '/api/missions')
api.add_resource(MissionResource, '/api/missions/<int:mission_id>')
api.add_resource(ApplicationResource, '/api/missions/<int:mission_id>/apply')
api.add_resource(UserMissionsResource, '/api/users/<int:user_id>/missions')
api.add_resource(UserApplicationsResource, '/api/users/<int:user_id>/applications')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)