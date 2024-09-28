from flask import Flask, render_template, redirect, url_for, flash, session, request
import uuid
from datetime import datetime

app = Flask(_name_)
app.secret_key = 'supersecretkey'

# Simulating an in-memory database
attendance_db = {}
session_urls = {}

# Teacher portal route
@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if 'generate_url' in session and session['generate_url']:
        flash(f"Generated Attendance URL: {request.host_url}student/{session['generate_url']}")
    
    return render_template('teacher.html')

# Endpoint to generate a unique URL
@app.route('/teacher/generate')
def generate_url():
    session_id = str(uuid.uuid4())
    session_urls[session_id] = {'created_at': datetime.now(), 'status': 'active'}
    
    session['generate_url'] = session_id
    flash(f"Attendance URL generated successfully!")
    return redirect(url_for('teacher'))

# Student portal to mark attendance
@app.route('/student/<session_id>')
def student(session_id):
    if session_id not in session_urls or session_urls[session_id]['status'] != 'active':
        return "Invalid or expired attendance session.", 400

    student_id = 'student_123'  # Simulated student ID; in a real app, students would log in.
    attendance_db[student_id] = {'status': 'Present', 'time': datetime.now()}
    
    flash('You have been marked present!')
    return redirect(url_for('student_page'))

# Student home page
@app.route('/student')
def student_page():
    return render_template('student.html')

if _name_ == '_main_':
    app.run(debug=True)