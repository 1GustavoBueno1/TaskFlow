from flask.blueprints import Blueprint
from flask import request, jsonify, session, Response, render_template
from app.models.user import UserRepository
from app.services.user_service import Usuario

usuario_bp = Blueprint('usuario', __name__, url_prefix='/perfil')
banco_usuario = UserRepository()
servico_usuario = Usuario()

@usuario_bp.route('/visualizar', methods=['GET'])
def visualizar_perfil() -> tuple[Response, int]:
    if request.method == 'GET':
        id_usuario = session.get('user_id')
        if id_usuario:
            usuario = banco_usuario.find(id_usuario)
            return jsonify({"nome": usuario['name'],
                            "email": usuario['gmail']}), 200
        return jsonify({"Erro": "Efetue login para continuar!"}), 401


@usuario_bp.route('/editar', methods=['PUT'])
def editar_perfil() -> tuple[Response, int]:
    if request.method == 'PUT':
        id_usuario = session.get('user_id')
        if id_usuario:
            dados = request.get_json()
            for chave, valor in dados.items():
                resposta, mensagem = servico_usuario.editar_perfil(chave, valor, id_usuario)
                if resposta:
                    return jsonify({"Sucesso": mensagem}), 200
                return jsonify({"Erro": mensagem}), 400
        return jsonify({"Erro": "Efetue login para prosseguir"}), 401
