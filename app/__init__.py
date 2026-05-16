from flask import Flask
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
    return app
