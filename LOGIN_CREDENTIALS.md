# Login Credentials for Testing

## Server URL
**http://localhost:8080**

---

## Faculty Login Credentials

Use these credentials to log in to the Faculty Admin Panel:

| Employee ID | Password     | Name              | Department        |
|-------------|--------------|-------------------|-------------------|
| **EMP001**  | faculty123   | Dr. Rajesh Kumar  | Computer Science  |
| **EMP002**  | password456  | Dr. Sunita Reddy  | Mathematics       |
| **EMP003**  | admin789     | Prof. Anil Sharma | Physics           |
| **EMP004**  | secure123    | Dr. Meera Patel   | Chemistry         |
| **sarthak11** | 123        | Sarthak Ghosh     | Computer Science  |

### How to Login as Faculty:
1. Open http://localhost:8080
2. Click on "Faculty Login" tab
3. Enter Employee ID (e.g., **sarthak11**)
4. Enter Password (e.g., **123**)
5. Click "Login to Admin Panel"
6. You will be redirected to the admin panel where you can:
   - View all students
   - Filter by course and year
   - Update marks and CGPA
   - See the class topper

---

## Student Roll Numbers

Use these roll numbers to check student grades:

| Roll Number | Name          | CGPA | Attendance | Degree |
|-------------|---------------|------|------------|--------|
| 20240101    | Rahul Kumar   | 8.5  | 92%        | B.Tech |
| **20240102**| **Priya Sharma** | **9.2** | **95%** | **B.Tech** ⭐ **TOPPER** |
| 20240103    | Sneha Gupta   | 8.8  | 90%        | B.Tech |
| 20240104    | Rohan Das     | 7.5  | 80%        | B.Tech |
| 20230201    | Amit Patel    | 7.8  | 88%        | B.Sc   |
| 20230202    | Vikram Singh  | 8.2  | 85%        | B.Sc   |
| 20230203    | Kavya Reddy   | 9.0  | 93%        | B.Sc   |
| 20220301    | Anjali Verma  | 9.5  | 98%        | M.Tech |
| 20260105    | Arjun Mehta   | 8.7  | 91%        | B.Tech |
| 20250301    | Ishita Bose   | 9.3  | 96%        | B.Sc   |

### How to Check Grades as Student:
1. Open http://localhost:8080
2. Stay on "Student Login" tab (default)
3. Enter Roll Number (e.g., **20240101**)
4. Click "Get My Grades"
5. View your complete academic report

---

## Troubleshooting

### Faculty Login Not Working?
1. **Check Server**: Make sure the server is running at http://localhost:8080
2. **Check Credentials**: Use exact Employee ID and Password (case-sensitive)
3. **Browser Console**: Press F12 and check Console tab for error messages
4. **Clear Cache**: Try clearing browser cache or use incognito/private mode
5. **Check Network**: Verify the API call to `/api/faculty/login` returns success

### Debug Mode
The updated code includes console.log statements. To debug:
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Try logging in
4. You'll see detailed logs of the login process

### API Testing
Test the API directly:
```bash
# Test faculty login
curl -X POST http://localhost:8080/api/faculty/login \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "EMP001", "password": "faculty123"}'

# Should return:
# {"department": "Computer Science", "employee_id": "EMP001", "name": "Dr. Rajesh Kumar", "success": true}
```

---

## Notes

- All passwords are hashed with SHA-256 before storage
- Faculty credentials are stored in `faculty_credentials.dat` (binary file)
- Student data is stored in `students_data.json`
- Sessions are maintained using browser sessionStorage
- The server includes detailed console logging for debugging
