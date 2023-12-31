import os
from flask import Flask, render_template
from flask_mysql_connector import MySQL
import cloudinary
# from config import CLOUD_NAME, CLOUD_API_KEY, CLOUD_SECRET_KEY

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_DATABASE'] = os.getenv("MYSQL_DATABASE")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
mysql = MySQL(app)
CLOUD_NAME=os.getenv("CLOUD_NAME")
CLOUD_API_KEY=os.getenv("CLOUD_API_KEY")
CLOUD_SECRET_KEY=os.getenv("CLOUD_SECRET_KEY")

cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=CLOUD_API_KEY,
        api_secret=CLOUD_SECRET_KEY,
    )


def create_app():
    
    from ssis.routes.student import student_bp
    from ssis.routes.college import college_bp
    from ssis.routes.course import course_bp
    
    @app.route("/")
    def home_page():
        return render_template("home.html")
    
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(course_bp, url_prefix='/course')
    app.register_blueprint(college_bp, url_prefix='/college')
    
    return app
