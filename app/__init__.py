from flask import Flask, render_template, session
from .config import Config
from .routes.auth_route import auth_bp
from .routes.task_route import tarefa_bp
from .routes.user_route import usuario_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefa_bp)
    app.register_blueprint(usuario_bp)
    @app.route('/')
    def homepage():
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        if user_id:
            return render_template('index_login.html', nome_de_usuario = user_name)
        return render_template('index.html')
    return app
