"""
Student Management System
Manages student records including roll no, name, marks, CGPA, grade, attendance, degree
"""
import pickle
import json
from datetime import datetime
from typing import List, Dict, Optional


class Student:
    """Student class to store student information"""
    
    def __init__(self, roll_no: str, name: str, marks: float, cgpa: float, 
                 attendance: float, degree: str):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks
        self.cgpa = cgpa
        self.attendance = attendance
        self.degree = degree
        self.grade = self.calculate_grade()
        self.year_of_registration = self.extract_year_from_roll()
        
    def calculate_grade(self) -> str:
        """Calculate grade based on CGPA"""
        if self.cgpa >= 9.0:
            return 'A+'
        elif self.cgpa >= 8.0:
            return 'A'
        elif self.cgpa >= 7.0:
            return 'B+'
        elif self.cgpa >= 6.0:
            return 'B'
        elif self.cgpa >= 5.0:
            return 'C'
        else:
            return 'F'
    
    def extract_year_from_roll(self) -> int:
        """Extract year of registration from roll number
        Assuming format: YYYYXXXX where YYYY is year"""
        try:
            # Extract first 4 digits as year
            year = int(self.roll_no[:4])
            return year
        except:
            return 2024  # Default year
    
    def get_remaining_years(self) -> int:
        """Calculate remaining years in college based on degree type"""
        current_year = datetime.now().year
        years_elapsed = current_year - self.year_of_registration
        
        # Standard degree durations
        degree_duration = {
            'B.Tech': 4,
            'B.Sc': 3,
            'M.Tech': 2,
            'M.Sc': 2,
            'MBA': 2,
            'BBA': 3,
            'BCA': 3,
            'MCA': 3
        }
        
        total_years = degree_duration.get(self.degree, 4)  # Default 4 years
        remaining = total_years - years_elapsed
        return max(0, remaining)  # Don't return negative values
    
    def to_dict(self) -> Dict:
        """Convert student object to dictionary"""
        return {
            'roll_no': self.roll_no,
            'name': self.name,
            'marks': self.marks,
            'cgpa': self.cgpa,
            'grade': self.grade,
            'attendance': self.attendance,
            'degree': self.degree,
            'year_of_registration': self.year_of_registration,
            'remaining_years': self.get_remaining_years()
        }
    
    def __str__(self) -> str:
        """String representation of student"""
        return f"""
Roll No: {self.roll_no}
Name: {self.name}
Marks: {self.marks}
CGPA: {self.cgpa}
Grade: {self.grade}
Attendance: {self.attendance}%
Degree: {self.degree}
Year of Registration: {self.year_of_registration}
Remaining Years: {self.get_remaining_years()}
"""


class StudentManagementSystem:
    """System to manage multiple students"""
    
    def __init__(self):
        self.students: List[Student] = []
        self.data_file = 'students_data.json'
        self.load_students()
    
    def add_student(self, roll_no: str, name: str, marks: float, cgpa: float, 
                    attendance: float, degree: str):
        """Add a new student to the system"""
        student = Student(roll_no, name, marks, cgpa, attendance, degree)
        self.students.append(student)
        self.save_students()
        return student
    
    def get_student_by_roll(self, roll_no: str) -> Optional[Student]:
        """Find student by roll number"""
        for student in self.students:
            if student.roll_no == roll_no:
                return student
        return None
    
    def update_marks(self, roll_no: str, marks: float, cgpa: float):
        """Update marks and CGPA for a student"""
        student = self.get_student_by_roll(roll_no)
        if student:
            student.marks = marks
            student.cgpa = cgpa
            student.grade = student.calculate_grade()
            self.save_students()
            return True
        return False
    
    def find_topper(self) -> Optional[Student]:
        """Find topper based on attendance and CGPA
        Priority: CGPA first, then attendance as tiebreaker"""
        if not self.students:
            return None
        
        # Filter students with minimum 75% attendance
        eligible_students = [s for s in self.students if s.attendance >= 75]
        
        if not eligible_students:
            return None
        
        # Sort by CGPA (descending) and attendance (descending)
        topper = max(eligible_students, key=lambda s: (s.cgpa, s.attendance))
        return topper
    
    def get_students_by_course(self, course_code: str) -> List[Student]:
        """Get students filtered by course code (degree type)"""
        return [s for s in self.students if course_code in s.degree]
    
    def get_students_by_year(self, year: int) -> List[Student]:
        """Get students by year of registration"""
        return [s for s in self.students if s.year_of_registration == year]
    
    def display_all_students(self):
        """Display all students"""
        if not self.students:
            print("No students in the system.")
            return
        
        print("\n" + "="*60)
        print("ALL STUDENTS")
        print("="*60)
        for student in self.students:
            print(student)
            print("-"*60)
    
    def save_students(self):
        """Save students data to JSON file"""
        data = [student.to_dict() for student in self.students]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_students(self):
        """Load students data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                for student_data in data:
                    student = Student(
                        student_data['roll_no'],
                        student_data['name'],
                        student_data['marks'],
                        student_data['cgpa'],
                        student_data['attendance'],
                        student_data['degree']
                    )
                    self.students.append(student)
        except FileNotFoundError:
            print("No existing student data found. Starting fresh.")


def create_sample_students():
    """Create sample students for demonstration"""
    sms = StudentManagementSystem()
    
    # Adding sample students
    sample_data = [
        ("20240101", "Rahul Kumar", 85.5, 8.5, 92.0, "B.Tech"),
        ("20240102", "Priya Sharma", 92.0, 9.2, 95.0, "B.Tech"),
        ("20230201", "Amit Patel", 78.0, 7.8, 88.0, "B.Sc"),
        ("20240103", "Sneha Gupta", 88.0, 8.8, 90.0, "B.Tech"),
        ("20230202", "Vikram Singh", 82.0, 8.2, 85.0, "B.Sc"),
        ("20220301", "Anjali Verma", 95.0, 9.5, 98.0, "M.Tech"),
        ("20240104", "Rohan Das", 75.0, 7.5, 80.0, "B.Tech"),
        ("20230203", "Kavya Reddy", 90.0, 9.0, 93.0, "B.Sc"),
    ]
    
    for roll, name, marks, cgpa, attendance, degree in sample_data:
        sms.add_student(roll, name, marks, cgpa, attendance, degree)
    
    return sms


def main():
    """Main function to demonstrate the system"""
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    
    # Create system with sample students
    sms = create_sample_students()
    
    # Display all students
    sms.display_all_students()
    
    # Find and display topper
    topper = sms.find_topper()
    if topper:
        print("\n" + "="*60)
        print("CLASS TOPPER (Based on CGPA and Attendance)")
        print("="*60)
        print(topper)
    
    # Example: Find specific student and show remaining years
    print("\n" + "="*60)
    print("STUDENT SEARCH EXAMPLE")
    print("="*60)
    roll_to_search = "20240102"
    student = sms.get_student_by_roll(roll_to_search)
    if student:
        print(f"\nSearching for Roll No: {roll_to_search}")
        print(student)
        print(f"\nThis student will be in college for {student.get_remaining_years()} more years.")
    
    # Students by year
    print("\n" + "="*60)
    print("STUDENTS REGISTERED IN 2024")
    print("="*60)
    students_2024 = sms.get_students_by_year(2024)
    for student in students_2024:
        print(f"{student.roll_no} - {student.name} ({student.degree})")


if __name__ == "__main__":
    main()
