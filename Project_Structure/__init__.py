from flask import Flask

def init_app():
    
    app = Flask(__name__)
    app.config['SECRET KEY'] = "TESTES3nTryMulTiW4y"
    
    from .views import views    
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    return app