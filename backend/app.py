from flask import Flask
from flask_cors import CORS
from routes.login import login_blueprint
from routes.profile import profile_blueprint
from routes.viewLogs import logs_blueprint
from routes.grading_config import grading_config_blueprint
from routes.getMessages import messages_blueprint
from routes.grade_upload_route import grade_upload_blueprint
from routes.grade_communication_route import grade_communication_blueprint
from routes.student_grade_handling_route import grade_reports_blueprint
from routes.overall_results import overall_results_blueprint
from routes.faculty_courses import faculty_courses_blueprint
from routes.search_grades import search_grades_blueprint
from routes.pdf_handling import pdf_handling_blueprint
app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(grading_config_blueprint)
app.register_blueprint(messages_blueprint)
app.register_blueprint(grade_upload_blueprint)
app.register_blueprint(grade_communication_blueprint)
app.register_blueprint(grade_reports_blueprint)
app.register_blueprint(overall_results_blueprint)
app.register_blueprint(faculty_courses_blueprint)
app.register_blueprint(search_grades_blueprint)
app.register_blueprint(pdf_handling_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
