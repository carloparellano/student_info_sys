import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
import cloudinary
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    app.config["DB_HOST"] = DB_HOST
    app.config["DB_USER"] = DB_USERNAME
    app.config["DB_PASSWORD"] = DB_PASSWORD
    app.config["DB_NAME"] = DB_NAME
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["BOOTSTRAP_SERVE_LOCAL"] = BOOTSTRAP_SERVE_LOCAL
    print(DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL)
    bootstrap.init_app(app)

    # Cloudinary config
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("CLOUD_API_KEY"),
        api_secret=os.getenv("CLOUD_SECRET_KEY"),
    )

    @app.route("/")
    def home_page():
        return render_template("home.html")

    # Import blueprints (CORRECT NAMES)
    from .students import student_bp
    from .colleges import college_bp
    from .courses import courses_bp
    
    # Register blueprints
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(courses_bp, url_prefix="/course")
    app.register_blueprint(college_bp, url_prefix="/college")

    CSRFProtect(app)
    return app