from app.services.chromadb_service import ChromaDBService
from flask import Blueprint, jsonify, request
from app.services.cohere_service import CohereService

app_bp = Blueprint('app', __name__)

cohere_service = CohereService(model="command-r")
chromadb_service = ChromaDBService()

@app_bp.route('/', methods=['GET'])
def index():
    return 'Question Answering API - Cohere'

@app_bp.route('/ask', methods=['POST'])
def ask():
    data = request.json

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid input format. Expected JSON object."}), 400
    
    question = data.get('question')
    user_name = data.get('user_name')
    
    if not question:
        return jsonify({"error": "Parameter 'question' is required."}), 400
    
    if not user_name:
        return jsonify({"error": "Parameter 'user_name' is required."}), 400

    try:
        response = cohere_service.get_answer(question)
        return jsonify({"answer": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app_bp.route('/init_db', methods=['POST'])
def init_db():
    try:
        chromadb_service.add_initial_document('./app/documents/documento.docx')
        return jsonify({"message": "Database initialized successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
