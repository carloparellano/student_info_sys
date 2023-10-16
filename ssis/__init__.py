from flask import Flask, render_template

app = Flask(__name__)

def create_app():
    
    from ssis.routes.student import student_bp
    
    @app.route("/")
    def home_page():
        return render_template("home.html")
    
    @app.route('/student/')
    def student():
        return render_template("student.html")
    
    @app.route('/course/')
    def course():
        return render_template("course.html")
    
    @app.route('/college/')
    def college():
        return render_template("college.html")
    
    app.register_blueprint(student_bp, url_prefix='/student')
    
    return app
