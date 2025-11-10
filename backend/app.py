# [file name]: app.py - CORRIGÉ
from dotenv import load_dotenv
import os
from flask import Flask
from models.models import db
from ressources.Module1_Register_User.freelance_ressource import *
from ressources.Module1_Register_User.user_ressource import *
from ressources.Module1_Register_User.ConnectionUserResource import *
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

# Routes freelances - ✅ TOUTES avec le préfixe /api
api.add_resource(FreelanceListResource, '/api/profiles')
api.add_resource(FreelanceResource, '/api/profiles/<int:user_id>')
#api.add_resource(PortfolioResource, '/api/profiles/<int:profile_id>/portfolio')
#api.add_resource(PortfolioItemResource, '/api/profiles/<int:profile_id>/portfolio')

# Routes Portfolio
api.add_resource(PortfolioListResource, '/api/profiles/<int:profile_id>/portfolio')              # GET all + POST
api.add_resource(PortfolioItemResource, '/api/profiles/<int:profile_id>/portfolio/<int:item_id>') # GET one + PUT + DELETE


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)