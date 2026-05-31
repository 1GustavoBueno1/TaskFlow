from flask import Flask, render_template, session, redirect, url_for, flash
from flask_limiter.errors import RateLimitExceeded
from .config import Config
from .extensions import csrf, limiter
from .routes.auth_route import auth_bp
from .routes.task_route import tarefa_bp
from .routes.user_route import usuario_bp
from .models.task import TaskRepository
from .models.user import UserRepository

table_user = UserRepository()
table_task = TaskRepository()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf.init_app(app)
    limiter.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefa_bp)
    app.register_blueprint(usuario_bp)

    @app.errorhandler(RateLimitExceeded)
    def handler_limite(e):
        flash("Muitas tentativas. Aguarde um momento e tente novamente.", "erro")
        return redirect(url_for('auth.login'))

    table_user.create_table_users()
    table_task.create_table_tasks()

    @app.route('/')
    def homepage():
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        if user_id:
            return render_template('index_login.html', nome_de_usuario=user_name)
        return render_template('index.html')

    return app
