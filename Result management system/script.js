let students = JSON.parse(localStorage.getItem('students')) || [];

document.getElementById('studentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const rollNo = document.getElementById('rollNo').value;
    const name = document.getElementById('name').value;
    const dob = document.getElementById('dob').value;
    const score = document.getElementById('score').value;

    let isValid = true;

    if (!rollNo) {
        document.getElementById('rollNoError').textContent = 'Roll No is required';
        isValid = false;
    } else {
        document.getElementById('rollNoError').textContent = '';
    }

    if (!name) {
        document.getElementById('nameError').textContent = 'Name is required';
        isValid = false;
    } else {
        document.getElementById('nameError').textContent = '';
    }

    const currentDate = new Date('2025-07-01T16:11:00Z'); // Current date and time: 04:11 PM IST, July 01, 2025
    const inputDob = new Date(dob);
    if (!dob) {
        document.getElementById('dobError').textContent = 'Date of Birth is required';
        isValid = false;
    } else if (inputDob >= currentDate) {
        document.getElementById('dobError').textContent = 'Please enter valid Date of Birth';
        isValid = false;
    } else {
        document.getElementById('dobError').textContent = '';
    }

    if (!score || score < 0 || score > 100) {
        document.getElementById('scoreError').textContent = 'Score must be between 0 and 100';
        isValid = false;
    } else {
        document.getElementById('scoreError').textContent = '';
    }

    if (isValid) {
        const existingStudentIndex = students.findIndex(student => student.rollNo === rollNo);
        const student = { rollNo, name, dob, score };

        if (existingStudentIndex !== -1) {
            // Update existing record
            students[existingStudentIndex] = student;
            alert('Student record updated successfully!');
        } else {
            // Add new record
            students.push(student);
            alert('Student result added successfully!');
        }
        localStorage.setItem('students', JSON.stringify(students));
        this.reset();
    }
});

function viewAll() {
    if (students.length === 0) {
        alert('No results available.');
    } else {
        localStorage.setItem('students', JSON.stringify(students));
        window.location.href = 'results.html';
    }
}

function goBack() {
    window.history.back();
}