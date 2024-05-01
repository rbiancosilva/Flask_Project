from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def init_app():
    
    app = Flask(__name__)
    app.secret_key = "TESTES3nTryMulTiW4y"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    
    from .views import views    
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    from .models import User, Movie, List, ListMovies

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'views.login_page'
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_id(id):
        return User.query.get(int(id))
    
    return app

        
