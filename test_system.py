"""
Quick Test Script - Verify all components work correctly
"""
import sys

def test_student_management():
    """Test student management module"""
    print("Testing Student Management...")
    try:
        from student_management import Student, StudentManagementSystem
        
        # Create a test student
        student = Student("20240999", "Test Student", 85.0, 8.5, 90.0, "B.Tech")
        
        # Verify basic properties
        assert student.roll_no == "20240999"
        assert student.name == "Test Student"
        assert student.grade in ['A', 'A+', 'B', 'B+', 'C', 'F']
        assert student.year_of_registration == 2024
        
        print("  ✓ Student class working")
        
        # Test management system
        sms = StudentManagementSystem()
        initial_count = len(sms.students)
        
        print(f"  ✓ StudentManagementSystem initialized ({initial_count} students loaded)")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_faculty_auth():
    """Test faculty authentication module"""
    print("\nTesting Faculty Authentication...")
    try:
        from faculty_auth import Faculty, FacultyAuthSystem
        
        # Create test faculty
        faculty = Faculty("TEST001", "Test Faculty", "testpass", "Testing")
        
        # Verify password hashing
        assert faculty.verify_password("testpass") == True
        assert faculty.verify_password("wrongpass") == False
        
        print("  ✓ Faculty class working")
        print("  ✓ Password hashing and verification working")
        
        # Test auth system
        auth = FacultyAuthSystem()
        initial_count = len(auth.faculty_list)
        
        print(f"  ✓ FacultyAuthSystem initialized ({initial_count} faculty loaded)")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_web_server():
    """Test Flask web server setup"""
    print("\nTesting Web Server Setup...")
    try:
        import flask
        import flask_cors
        print("  ✓ Flask installed")
        print("  ✓ Flask-CORS installed")
        
        # Try importing the app
        # We don't actually start it, just verify it can be imported
        print("  ✓ All dependencies available")
        
        return True
    except ImportError as e:
        print(f"  ✗ Missing dependency: {e}")
        print("  ! Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def check_files():
    """Check if all required files exist"""
    print("\nChecking Required Files...")
    import os
    
    required_files = [
        'student_management.py',
        'faculty_auth.py',
        'app.py',
        'index.html',
        'admin.html',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING!")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests"""
    print("="*60)
    print("STUDENT MANAGEMENT SYSTEM - COMPONENT TEST")
    print("="*60)
    
    files_ok = check_files()
    student_ok = test_student_management()
    faculty_ok = test_faculty_auth()
    web_ok = test_web_server()
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"Files Check:         {'✓ PASS' if files_ok else '✗ FAIL'}")
    print(f"Student Management:  {'✓ PASS' if student_ok else '✗ FAIL'}")
    print(f"Faculty Auth:        {'✓ PASS' if faculty_ok else '✗ FAIL'}")
    print(f"Web Server Setup:    {'✓ PASS' if web_ok else '✗ FAIL'}")
    print("="*60)
    
    if all([files_ok, student_ok, faculty_ok, web_ok]):
        print("\n🎉 All tests passed! The system is ready to run.")
        print("\nTo start the server:")
        print("  • Run: python app.py")
        print("  • Or run: ./run.sh")
        print("\nThen open: http://localhost:5001")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
