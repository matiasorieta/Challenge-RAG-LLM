from flask import Flask
from .routes import app_bp  # Importa el blueprint de las rutas
from app.services.cohere_service import CohereService

cohere_service = CohereService()

def create_app():
    app = Flask(__name__)

    # Registra el blueprint
    app.register_blueprint(app_bp)

    return app
