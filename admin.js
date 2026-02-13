        let allStudents = [];
        let filteredStudents = [];

        // Check authentication on page load
        window.onload = function() {
            console.log('Admin page loaded, checking authentication...');
            const facultyId = sessionStorage.getItem('facultyId');
            const facultyName = sessionStorage.getItem('facultyName');
            console.log('Faculty ID from session:', facultyId);
            console.log('Faculty Name from session:', facultyName);

            if (!facultyId) {
                console.log('No faculty ID found, showing authentication required message');
                document.getElementById('authRequired').style.display = 'block';
                document.getElementById('adminPanel').style.display = 'none';
            } else {
                console.log('Faculty authenticated, loading admin panel');
                document.getElementById('authRequired').style.display = 'none';
                document.getElementById('adminPanel').style.display = 'block';
                document.getElementById('facultyName').textContent = facultyName || 'Faculty';
                loadStudents();
                loadTopper();
            }
        };

        function logout() {
            sessionStorage.clear();
            window.location.href = 'index.html';
        }

        async function loadStudents() {
            console.log('Loading students...');
            try {
                const response = await fetch('/api/students');
                console.log('Students API response status:', response.status);
                const data = await response.json();
                console.log('Students data received:', data);
                
                if (response.ok) {
                    allStudents = data.students;
                    filteredStudents = [...allStudents];
                    displayStudents();
                    updateStats();
                    console.log('Students loaded successfully:', allStudents.length);
                } else {
                    console.error('Failed to load students:', data);
                    showMessage('Error loading students', 'error');
                }
            } catch (error) {
                console.error('Error loading students:', error);
                showMessage('Error loading students: ' + error.message, 'error');
            }
        }

        async function loadTopper() {
            try {
                const response = await fetch('/api/topper');
                const data = await response.json();
                
                if (response.ok && data.topper) {
                    document.getElementById('topperName').textContent = data.topper.name;
                    document.getElementById('topperRoll').textContent = data.topper.roll_no;
                    document.getElementById('topperCGPA').textContent = data.topper.cgpa;
                    document.getElementById('topperAttendance').textContent = data.topper.attendance + '%';
                    document.getElementById('topperGrade').textContent = data.topper.grade;
                }
            } catch (error) {
                console.error('Error loading topper:', error);
            }
        }

        function displayStudents() {
            const tbody = document.getElementById('studentTableBody');
            tbody.innerHTML = '';

            filteredStudents.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="checkbox" class="student-checkbox" data-roll="${student.roll_no}" onchange="updateSelectedCount()"></td>
                    <td>${student.roll_no}</td>
                    <td>${student.name}</td>
                    <td>${student.degree}</td>
                    <td>${student.year_of_registration}</td>
                    <td>${student.marks}</td>
                    <td><input type="number" class="new-marks" data-roll="${student.roll_no}" min="0" max="100" step="0.1"></td>
                    <td>${student.cgpa}</td>
                    <td><input type="number" class="new-cgpa" data-roll="${student.roll_no}" min="0" max="10" step="0.01"></td>
                    <td>${student.attendance}%</td>
                    <td><span style="background: #667eea; color: white; padding: 4px 12px; border-radius: 12px;">${student.grade}</span></td>
                `;
                tbody.appendChild(row);
            });
        }

        function filterStudents() {
            const courseFilter = document.getElementById('courseFilter').value;
            const yearFilter = document.getElementById('yearFilter').value;
            const searchFilter = document.getElementById('searchFilter').value.toLowerCase();

            filteredStudents = allStudents.filter(student => {
                const courseMatch = !courseFilter || student.degree === courseFilter;
                const yearMatch = !yearFilter || student.year_of_registration.toString() === yearFilter;
                const searchMatch = !searchFilter || 
                    student.name.toLowerCase().includes(searchFilter) || 
                    student.roll_no.toLowerCase().includes(searchFilter);

                return courseMatch && yearMatch && searchMatch;
            });

            displayStudents();
            updateStats();
        }

        function updateStats() {
            document.getElementById('totalStudents').textContent = filteredStudents.length;
            
            if (filteredStudents.length > 0) {
                const avgCGPA = filteredStudents.reduce((sum, s) => sum + s.cgpa, 0) / filteredStudents.length;
                document.getElementById('avgCGPA').textContent = avgCGPA.toFixed(2);
            } else {
                document.getElementById('avgCGPA').textContent = '0.0';
            }
        }

        function updateSelectedCount() {
            const selected = document.querySelectorAll('.student-checkbox:checked').length;
            document.getElementById('selectedCount').textContent = selected;
        }

        function selectAll() {
            document.querySelectorAll('.student-checkbox').forEach(cb => cb.checked = true);
            updateSelectedCount();
        }

        function deselectAll() {
            document.querySelectorAll('.student-checkbox').forEach(cb => cb.checked = false);
            updateSelectedCount();
        }

        async function saveMarks() {
            const selectedCheckboxes = document.querySelectorAll('.student-checkbox:checked');
            
            if (selectedCheckboxes.length === 0) {
                showMessage('Please select at least one student', 'error');
                return;
            }

            const updates = [];
            selectedCheckboxes.forEach(checkbox => {
                const rollNo = checkbox.dataset.roll;
                const newMarks = document.querySelector(`.new-marks[data-roll="${rollNo}"]`).value;
                const newCGPA = document.querySelector(`.new-cgpa[data-roll="${rollNo}"]`).value;

                if (newMarks || newCGPA) {
                    updates.push({
                        roll_no: rollNo,
                        marks: newMarks ? parseFloat(newMarks) : null,
                        cgpa: newCGPA ? parseFloat(newCGPA) : null
                    });
                }
            });

            if (updates.length === 0) {
                showMessage('Please enter marks or CGPA for selected students', 'error');
                return;
            }

            try {
                const response = await fetch('/api/update-marks', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ updates: updates })
                });

                const data = await response.json();

                if (response.ok) {
                    showMessage(`Successfully updated ${data.updated_count} student(s)`, 'success');
                    loadStudents();
                    loadTopper();
                    deselectAll();
                } else {
                    showMessage('Error updating marks', 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('Error updating marks', 'error');
            }
        }

        function showMessage(message, type) {
            const messageBox = document.getElementById('messageBox');
            messageBox.textContent = message;
            messageBox.className = `message ${type} show`;
            
            setTimeout(() => {
                messageBox.classList.remove('show');
            }, 5000);
        }