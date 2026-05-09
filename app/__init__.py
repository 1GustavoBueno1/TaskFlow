from flask import Flask
from .config import Config
from .routes.auth_route import auth_bp
from .routes.task_route import task_bp
from .routes.user_route import user_bp
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    return app