from flask.blueprints import Blueprint
from flask import request, jsonify, session
from app.models.user import UserRepository
from app.services.user_service import User
user_bp = Blueprint('user', __name__, url_prefix = '/profile')
user_db = UserRepository()
user_service = User()
@user_bp.route('/View', methods = ['GET'])
def view_profile() -> dict:
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            user = user_db.find(user_id)
            return jsonify({"Nome": user['name'], 
                            "email": user['gmail']})
        return jsonify({"Erro": 'Efetue login para continuar!'})
@user_bp.route('/EditUserProfile', methods = ['PUT'])
def edit_profile() -> tuple[bool, str]:
    if request.method == 'PUT':
        user_id = session.get('user_id')
        if user_id:
            dados_postman = request.get_json()
            for key, value in dados_postman.items():
                resposta, msg = user_service.edit_profile(key, value, user_id)
                if resposta:
                    return jsonify({"Sucesso": msg})
                return jsonify({"Erro": msg})
        return jsonify({"Erro": "Efetue login para prosseguir"})
        