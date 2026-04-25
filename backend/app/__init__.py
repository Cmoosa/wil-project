from flask import Flask
from flask_cors import CORS
from .config import Config
from .json_db import init_db
from .routes.auth_routes import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "apex-enterprise-secret"


    CORS(app)

    init_db(Config.DB_PATH)

    from .routes.vendor_routes import bp as vendor_bp
    from .routes.po_routes import bp as po_bp
    from .routes.ai_routes import bp as ai_bp

    app.register_blueprint(vendor_bp)
    app.register_blueprint(po_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(auth_bp)


    return app
