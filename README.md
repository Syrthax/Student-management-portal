# Student Management System

A comprehensive web-based student management system with faculty authentication, student grade checking, and admin panel for managing student records.

## Features

### For Students
- 🎓 Check grades by entering roll number
- 📊 View CGPA, marks, attendance, and grade
- 📅 See year of registration and remaining years in college
- 🌐 Clean, responsive web interface

### For Faculty
- 🔐 Secure login with employee ID and password (stored in binary .dat file)
- 📝 Update marks and CGPA for students
- 🔍 Filter students by course code and year of registration
- ✅ Select multiple students using checkboxes
- 🏆 View class topper based on CGPA and attendance
- 📈 View statistics and student data

### Backend Features
- 👨‍🎓 Complete student information management
- 🔢 Automatic grade calculation based on CGPA
- 📆 Year extraction from roll number
- ⏱️ Remaining years calculation based on degree type
- 🥇 Topper identification based on attendance and CGPA
- 💾 Data persistence with JSON and binary files

## Project Structure

```
today/
├── app.py                      # Flask web server
├── student_management.py       # Student management module
├── faculty_auth.py             # Faculty authentication system
├── index.html                  # Student portal (home page)
├── admin.html                  # Faculty admin panel
├── requirements.txt            # Python dependencies
├── students_data.json          # Student data storage (auto-generated)
└── faculty_credentials.dat     # Faculty credentials in binary format (auto-generated)
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Run the Web Server (Recommended)

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - Open your browser and go to: `http://localhost:5001`
   - For students: Use the Student Login tab
   - For faculty: Use the Faculty Login tab or go directly to admin panel

### Option 2: Run Standalone Python Scripts

1. **Test Student Management:**
   ```bash
   python student_management.py
   ```

2. **Test Faculty Authentication:**
   ```bash
   python faculty_auth.py
   ```

## Sample Credentials

### Faculty Login (for admin panel)
| Employee ID | Password     | Name              | Department        |
|-------------|--------------|-------------------|-------------------|
| EMP001      | faculty123   | Dr. Rajesh Kumar  | Computer Science  |
| EMP002      | password456  | Dr. Sunita Reddy  | Mathematics       |
| EMP003      | admin789     | Prof. Anil Sharma | Physics           |
| EMP004      | secure123    | Dr. Meera Patel   | Chemistry         |

### Student Roll Numbers (for checking grades)
- 20240101 - Rahul Kumar (B.Tech, CGPA: 8.5)
- 20240102 - Priya Sharma (B.Tech, CGPA: 9.2)
- 20230201 - Amit Patel (B.Sc, CGPA: 7.8)
- 20240103 - Sneha Gupta (B.Tech, CGPA: 8.8)
- 20240104 - Rohan Das (B.Tech, CGPA: 7.5)

## How to Use

### Student Portal (index.html)

1. Navigate to the Student Login tab
2. Enter your roll number (e.g., 20240101)
3. Click "Get My Grades"
4. View your complete academic report including:
   - CGPA and Grade
   - Marks and Attendance
   - Year of Registration
   - Remaining years in college

### Faculty Admin Panel (admin.html)

1. Click on "Faculty Login" tab or go to admin panel
2. Enter your Employee ID and Password
3. After login, you can:
   - **View Class Topper**: See the best student based on CGPA and attendance
   - **Filter Students**: By course code, year, or search by name/roll number
   - **Update Marks**: 
     - Select students using checkboxes
     - Enter new marks and/or CGPA
     - Click "Save Marks for Selected Students"
   - **View Statistics**: Total students, average CGPA, etc.

## System Features

### Student Information Includes:
- Roll Number
- Name
- Marks
- CGPA
- Grade (automatically calculated)
- Attendance Percentage
- Degree/Course
- Year of Registration (extracted from roll number)
- Remaining Years in College (calculated based on degree duration)

### Topper Selection Criteria:
1. Minimum 75% attendance required
2. Sorted by CGPA (descending)
3. Attendance used as tiebreaker

### Grading System:
- **A+**: CGPA ≥ 9.0
- **A**: CGPA ≥ 8.0
- **B+**: CGPA ≥ 7.0
- **B**: CGPA ≥ 6.0
- **C**: CGPA ≥ 5.0
- **F**: CGPA < 5.0

### Roll Number Format:
The system expects roll numbers in format: `YYYYXXXX`
- First 4 digits (YYYY) represent the year of registration
- Example: 20240101 means student registered in 2024

### Degree Durations:
- B.Tech: 4 years
- B.Sc: 3 years
- M.Tech: 2 years
- M.Sc: 2 years
- MBA: 2 years
- BBA: 3 years
- BCA: 3 years
- MCA: 3 years

## API Endpoints

### Student Endpoints
- `GET /api/student/<roll_no>` - Get student by roll number
- `GET /api/students` - Get all students
- `GET /api/topper` - Get class topper
- `GET /api/students/course/<course_code>` - Filter by course
- `GET /api/students/year/<year>` - Filter by year
- `POST /api/add-student` - Add new student

### Faculty Endpoints
- `POST /api/faculty/login` - Faculty authentication
- `POST /api/update-marks` - Update student marks

### Other Endpoints
- `GET /api/health` - Health check

## Security Features

- Faculty passwords are hashed using SHA-256
- Credentials stored in binary format (.dat file)
- Session-based authentication for admin panel
- CORS enabled for API access

## Data Persistence

- **students_data.json**: Stores all student information in JSON format
- **faculty_credentials.dat**: Stores faculty credentials in binary format using pickle
- Both files are automatically created and updated by the system

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: JSON (students), Binary/Pickle (faculty credentials)
- **Authentication**: SHA-256 password hashing
- **API**: RESTful API with Flask

## Customization

### Adding New Students
You can add students via the API or by modifying the `create_sample_students()` function in `student_management.py`.

### Adding New Faculty
Add faculty via the API or by modifying the `create_sample_faculty()` function in `faculty_auth.py`.

### Changing Degree Durations
Modify the `degree_duration` dictionary in the `Student.get_remaining_years()` method.

## Troubleshooting

1. **Port already in use**: Change the port in `app.py` from 5000 to another port
2. **Module not found**: Make sure all dependencies are installed: `pip install -r requirements.txt`
3. **Data not loading**: Delete `.json` and `.dat` files to reset with sample data

## License

This project is created for educational purposes.

## Author

Created as a comprehensive student management system demonstration.
