import os
from flask import Flask, render_template
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_DATABASE'] = os.getenv("MYSQL_DATABASE")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
mysql = MySQL(app)



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
