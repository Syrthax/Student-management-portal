"""
Flask Web Server for Student Management System
Integrates student management, faculty authentication, and web interface
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from student_management import StudentManagementSystem
from faculty_auth import FacultyAuthSystem

app = Flask(__name__)
CORS(app)

# Initialize systems
sms = StudentManagementSystem()
auth_system = FacultyAuthSystem()

# Serve static HTML files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def index_page():
    return send_from_directory('.', 'index.html')

@app.route('/admin.html')
def admin_page():
    return send_from_directory('.', 'admin.html')


# API Endpoints

# Student endpoints
@app.route('/api/student/<roll_no>', methods=['GET'])
def get_student(roll_no):
    """Get student information by roll number"""
    student = sms.get_student_by_roll(roll_no)
    
    if student:
        return jsonify(student.to_dict()), 200
    else:
        return jsonify({'error': 'Student not found'}), 404


@app.route('/api/students', methods=['GET'])
def get_all_students():
    """Get all students"""
    students_data = [student.to_dict() for student in sms.students]
    return jsonify({'students': students_data}), 200


@app.route('/api/topper', methods=['GET'])
def get_topper():
    """Get class topper based on CGPA and attendance"""
    topper = sms.find_topper()
    
    if topper:
        return jsonify({'topper': topper.to_dict()}), 200
    else:
        return jsonify({'error': 'No topper found'}), 404


@app.route('/api/students/course/<course_code>', methods=['GET'])
def get_students_by_course(course_code):
    """Get students by course code"""
    students = sms.get_students_by_course(course_code)
    students_data = [student.to_dict() for student in students]
    return jsonify({'students': students_data}), 200


@app.route('/api/students/year/<int:year>', methods=['GET'])
def get_students_by_year(year):
    """Get students by year of registration"""
    students = sms.get_students_by_year(year)
    students_data = [student.to_dict() for student in students]
    return jsonify({'students': students_data}), 200


# Faculty endpoints
@app.route('/api/faculty/login', methods=['POST'])
def faculty_login():
    """Faculty login endpoint"""
    data = request.json
    employee_id = data.get('employee_id')
    password = data.get('password')
    
    if not employee_id or not password:
        return jsonify({'error': 'Employee ID and password required'}), 400
    
    if auth_system.authenticate(employee_id, password):
        faculty = auth_system.get_faculty(employee_id)
        return jsonify({
            'success': True,
            'name': faculty.name,
            'employee_id': faculty.employee_id,
            'department': faculty.department
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/update-marks', methods=['POST'])
def update_marks():
    """Update marks for multiple students"""
    data = request.json
    updates = data.get('updates', [])
    
    if not updates:
        return jsonify({'error': 'No updates provided'}), 400
    
    updated_count = 0
    for update in updates:
        roll_no = update.get('roll_no')
        new_marks = update.get('marks')
        new_cgpa = update.get('cgpa')
        
        student = sms.get_student_by_roll(roll_no)
        if student:
            if new_marks is not None:
                student.marks = new_marks
            if new_cgpa is not None:
                student.cgpa = new_cgpa
                student.grade = student.calculate_grade()
            updated_count += 1
    
    sms.save_students()
    
    return jsonify({
        'success': True,
        'updated_count': updated_count
    }), 200


@app.route('/api/add-student', methods=['POST'])
def add_student():
    """Add a new student"""
    data = request.json
    
    try:
        student = sms.add_student(
            roll_no=data['roll_no'],
            name=data['name'],
            marks=float(data['marks']),
            cgpa=float(data['cgpa']),
            attendance=float(data['attendance']),
            degree=data['degree']
        )
        return jsonify({
            'success': True,
            'student': student.to_dict()
        }), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'total_students': len(sms.students),
        'total_faculty': len(auth_system.faculty_list)
    }), 200


def initialize_data():
    """Initialize sample data if no data exists"""
    if len(sms.students) == 0:
        print("Initializing sample student data...")
        sample_students = [
            ("20240101", "Rahul Kumar", 85.5, 8.5, 92.0, "B.Tech"),
            ("20240102", "Priya Sharma", 92.0, 9.2, 95.0, "B.Tech"),
            ("20230201", "Amit Patel", 78.0, 7.8, 88.0, "B.Sc"),
            ("20240103", "Sneha Gupta", 88.0, 8.8, 90.0, "B.Tech"),
            ("20230202", "Vikram Singh", 82.0, 8.2, 85.0, "B.Sc"),
            ("20220301", "Anjali Verma", 95.0, 9.5, 98.0, "M.Tech"),
            ("20240104", "Rohan Das", 75.0, 7.5, 80.0, "B.Tech"),
            ("20230203", "Kavya Reddy", 90.0, 9.0, 93.0, "B.Sc"),
            ("20260105", "Arjun Mehta", 87.0, 8.7, 91.0, "B.Tech"),
            ("20250301", "Ishita Bose", 93.0, 9.3, 96.0, "B.Sc"),
        ]
        
        for roll, name, marks, cgpa, attendance, degree in sample_students:
            sms.add_student(roll, name, marks, cgpa, attendance, degree)
    
    if len(auth_system.faculty_list) == 0:
        print("Initializing sample faculty data...")
        sample_faculty = [
            ("EMP001", "Dr. Rajesh Kumar", "faculty123", "Computer Science"),
            ("EMP002", "Dr. Sunita Reddy", "password456", "Mathematics"),
            ("EMP003", "Prof. Anil Sharma", "admin789", "Physics"),
            ("EMP004", "Dr. Meera Patel", "secure123", "Chemistry"),
        ]
        
        for emp_id, name, password, dept in sample_faculty:
            auth_system.add_faculty(emp_id, name, password, dept)


if __name__ == '__main__':
    print("="*60)
    print("STUDENT MANAGEMENT SYSTEM - WEB SERVER")
    print("="*60)
    
    # Initialize sample data
    initialize_data()
    
    print("\nServer Information:")
    print(f"Total Students: {len(sms.students)}")
    print(f"Total Faculty: {len(auth_system.faculty_list)}")
    print("\nSample Faculty Credentials:")
    print("Employee ID: EMP001, Password: faculty123")
    print("Employee ID: EMP002, Password: password456")
    print("\nSample Student Roll Numbers:")
    print("20240101, 20240102, 20240103, 20240104")
    print("\n" + "="*60)
    print("Starting server at http://localhost:8080")
    print("="*60 + "\n")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=8080)
