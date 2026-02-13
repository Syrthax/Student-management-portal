"""
Faculty Authentication System
Stores faculty credentials in binary format (.dat file)
"""
import pickle
import hashlib
from typing import Dict, Optional, List


class Faculty:
    """Faculty class to store faculty information"""
    
    def __init__(self, employee_id: str, name: str, password: str, department: str):
        self.employee_id = employee_id
        self.name = name
        self.password_hash = self.hash_password(password)
        self.department = department
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches"""
        return self.password_hash == self.hash_password(password)
    
    def to_dict(self) -> Dict:
        """Convert faculty to dictionary"""
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'password_hash': self.password_hash,
            'department': self.department
        }


class FacultyAuthSystem:
    """System to manage faculty authentication"""
    
    def __init__(self, dat_file: str = 'faculty_credentials.dat'):
        self.dat_file = dat_file
        self.faculty_list: List[Faculty] = []
        self.load_credentials()
    
    def add_faculty(self, employee_id: str, name: str, password: str, department: str):
        """Add a new faculty member"""
        faculty = Faculty(employee_id, name, password, department)
        self.faculty_list.append(faculty)
        self.save_credentials()
        return faculty
    
    def authenticate(self, employee_id: str, password: str) -> bool:
        """Authenticate faculty by employee ID and password"""
        for faculty in self.faculty_list:
            if faculty.employee_id == employee_id:
                return faculty.verify_password(password)
        return False
    
    def get_faculty(self, employee_id: str) -> Optional[Faculty]:
        """Get faculty by employee ID"""
        for faculty in self.faculty_list:
            if faculty.employee_id == employee_id:
                return faculty
        return None
    
    def save_credentials(self):
        """Save faculty credentials to binary .dat file"""
        data = [faculty.to_dict() for faculty in self.faculty_list]
        with open(self.dat_file, 'wb') as f:
            pickle.dump(data, f)
        print(f"Faculty credentials saved to {self.dat_file}")
    
    def load_credentials(self):
        """Load faculty credentials from binary .dat file"""
        try:
            with open(self.dat_file, 'rb') as f:
                data = pickle.load(f)
                self.faculty_list = []
                for faculty_data in data:
                    faculty = Faculty.__new__(Faculty)
                    faculty.employee_id = faculty_data['employee_id']
                    faculty.name = faculty_data['name']
                    faculty.password_hash = faculty_data['password_hash']
                    faculty.department = faculty_data['department']
                    self.faculty_list.append(faculty)
            print(f"Loaded {len(self.faculty_list)} faculty members from {self.dat_file}")
        except FileNotFoundError:
            print("No existing faculty credentials found. Creating new file.")
    
    def display_all_faculty(self):
        """Display all faculty (without passwords)"""
        print("\n" + "="*60)
        print("ALL FACULTY MEMBERS")
        print("="*60)
        for faculty in self.faculty_list:
            print(f"Employee ID: {faculty.employee_id}")
            print(f"Name: {faculty.name}")
            print(f"Department: {faculty.department}")
            print("-"*60)


def create_sample_faculty():
    """Create sample faculty members"""
    auth_system = FacultyAuthSystem()
    
    # Add sample faculty
    sample_faculty = [
        ("EMP001", "Dr. Rajesh Kumar", "faculty123", "Computer Science"),
        ("EMP002", "Dr. Sunita Reddy", "password456", "Mathematics"),
        ("EMP003", "Prof. Anil Sharma", "admin789", "Physics"),
        ("EMP004", "Dr. Meera Patel", "secure123", "Chemistry"),
    ]
    
    for emp_id, name, password, dept in sample_faculty:
        auth_system.add_faculty(emp_id, name, password, dept)
    
    return auth_system


def main():
    """Main function to demonstrate faculty authentication"""
    print("FACULTY AUTHENTICATION SYSTEM")
    print("="*60)
    
    # Create sample faculty
    auth_system = create_sample_faculty()
    
    # Display all faculty
    auth_system.display_all_faculty()
    
    # Test authentication
    print("\n" + "="*60)
    print("AUTHENTICATION TEST")
    print("="*60)
    
    # Valid login
    test_id = "EMP001"
    test_pass = "faculty123"
    print(f"\nTesting: {test_id} with password '{test_pass}'")
    if auth_system.authenticate(test_id, test_pass):
        print("✓ Authentication successful!")
        faculty = auth_system.get_faculty(test_id)
        print(f"Welcome, {faculty.name} ({faculty.department})")
    else:
        print("✗ Authentication failed!")
    
    # Invalid login
    print(f"\nTesting: {test_id} with wrong password")
    if auth_system.authenticate(test_id, "wrongpassword"):
        print("✓ Authentication successful!")
    else:
        print("✗ Authentication failed!")


if __name__ == "__main__":
    main()
