        function switchTab(tab) {
            // Update tab buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tab + '-tab').classList.add('active');

            // Hide any error messages
            document.querySelectorAll('.error-message').forEach(msg => {
                msg.classList.remove('show');
            });
        }

        async function checkGrades(event) {
            event.preventDefault();
            
            const rollNo = document.getElementById('rollNo').value.trim();
            const resultCard = document.getElementById('studentResult');
            const errorMsg = document.getElementById('studentError');
            
            // Hide previous results
            resultCard.classList.remove('show');
            errorMsg.classList.remove('show');

            try {
                const response = await fetch(`/api/student/${rollNo}`);
                const data = await response.json();

                if (response.ok) {
                    // Display student data
                    document.getElementById('displayRollNo').textContent = data.roll_no;
                    document.getElementById('displayName').textContent = data.name;
                    document.getElementById('displayDegree').textContent = data.degree;
                    document.getElementById('displayMarks').textContent = data.marks;
                    document.getElementById('displayCGPA').textContent = data.cgpa;
                    document.getElementById('displayAttendance').textContent = data.attendance + '%';
                    document.getElementById('displayYear').textContent = data.year_of_registration;
                    document.getElementById('displayRemaining').textContent = data.remaining_years + ' year(s)';
                    
                    // Display grade with styling
                    const gradeElement = document.getElementById('displayGrade');
                    const gradeClass = 'grade-' + data.grade.replace('+', '-plus');
                    gradeElement.innerHTML = `<span class="grade-badge ${gradeClass}">${data.grade}</span>`;
                    
                    resultCard.classList.add('show');
                } else {
                    errorMsg.classList.add('show');
                }
            } catch (error) {
                console.error('Error:', error);
                errorMsg.classList.add('show');
            }
        }

        async function facultyLogin(event) {
            event.preventDefault();
            
            const employeeId = document.getElementById('employeeId').value.trim();
            const password = document.getElementById('password').value;
            const errorMsg = document.getElementById('facultyError');
            
            errorMsg.classList.remove('show');

            console.log('Attempting faculty login:', employeeId);

            try {
                const response = await fetch('/api/faculty/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ employee_id: employeeId, password: password })
                });

                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);

                if (response.ok) {
                    // Store session and redirect to admin panel
                    console.log('Login successful, storing session');
                    sessionStorage.setItem('facultyId', employeeId);
                    sessionStorage.setItem('facultyName', data.name);
                    console.log('Session stored, redirecting to admin.html');
                    window.location.href = '/admin.html';
                } else {
                    console.error('Login failed:', data.error);
                    errorMsg.textContent = data.error || 'Invalid credentials! Please check your Employee ID and password.';
                    errorMsg.classList.add('show');
                }
            } catch (error) {
                console.error('Network or parsing error:', error);
                errorMsg.textContent = 'Network error! Please check if the server is running.';
                errorMsg.classList.add('show');
            }
        }