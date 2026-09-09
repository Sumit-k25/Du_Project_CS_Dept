from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from functools import wraps
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tic_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============= ROUTES =============

@app.route('/')
def index():
    if 'tic_email' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        tic_email = data.get('tic_email')
        password = data.get('password')

        try:
            # Query Users table to authenticate
            response = supabase.table('Users').select('*').eq('tic_mail', tic_email).execute()
            
            if response.data and len(response.data) > 0:
                user = response.data[0]
                # In production, use proper password hashing (bcrypt, etc.)
                if user['password'] == password:
                    # Fetch college details
                    college_response = supabase.table('College_Details').select('*').eq('Tic_Email', tic_email).execute()
                    
                    if college_response.data and len(college_response.data) > 0:
                        college = college_response.data[0]
                        session['tic_email'] = tic_email
                        session['college_id'] = college['College_Code']
                        session['college_name'] = college['College_Name']
                        return jsonify({'success': True, 'message': 'Login successful'}), 200
                    else:
                        return jsonify({'success': False, 'message': 'College not found'}), 401
                else:
                    return jsonify({'success': False, 'message': 'Invalid password'}), 401
            else:
                return jsonify({'success': False, 'message': 'User not found'}), 401
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    college_id = session.get('college_id')
    college_name = session.get('college_name')
    
    try:
        # Fetch all teaching details for this college
        response = supabase.table('College_Course_Teaching_Details').select('*').eq('College_id', college_id).execute()
        entries = response.data if response.data else []
    except Exception as e:
        print(f"Error fetching entries: {str(e)}")
        entries = []
    
    return render_template('dashboard.html', 
                         college_name=college_name,
                         entries=entries)

@app.route('/api/add-entry', methods=['POST'])
@login_required
def add_entry():
    try:
        data = request.get_json()
        college_id = session.get('college_id')
        
        # Prepare data for insertion
        course_id = data.get('course_id')
        entry_data = {
            'College_id': college_id,
            'Course_id': int(course_id) if course_id and course_id.strip() else 1,  # Use default 1 if empty
            'Semester': int(data.get('semester')),
            'Paper_type': data.get('paper_type'),
            'paper_name': data.get('paper_name'),
            'UPC_code': data.get('upc_code'),
            'Teacher_Name': data.get('teacher_name'),
            'Theory_Practical': data.get('theory_practical'),
            'Teacher_Status': data.get('teacher_status'),
        }
        
        # Insert into Supabase
        response = supabase.table('College_Course_Teaching_Details').insert(entry_data).execute()
        
        if response.data:
            return jsonify({'success': True, 'message': 'Entry added successfully', 'data': response.data[0]}), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to add entry'}), 400
            
    except Exception as e:
        print(f"Error adding entry: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/entries/<college_id>')
@login_required
def get_entries(college_id):
    try:
        # Verify user belongs to this college
        if int(college_id) != session.get('college_id'):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        response = supabase.table('College_Course_Teaching_Details').select('*').eq('College_id', college_id).execute()
        entries = response.data if response.data else []
        
        return jsonify({'success': True, 'data': entries}), 200
        
    except Exception as e:
        print(f"Error fetching entries: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/delete-entry/<entry_id>', methods=['DELETE'])
@login_required
def delete_entry(entry_id):
    try:
        # First verify the entry belongs to this college
        response = supabase.table('College_Course_Teaching_Details').select('*').eq('id', entry_id).execute()
        
        if not response.data or response.data[0]['College_id'] != session.get('college_id'):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Delete the entry
        supabase.table('College_Course_Teaching_Details').delete().eq('id', entry_id).execute()
        
        return jsonify({'success': True, 'message': 'Entry deleted successfully'}), 200
        
    except Exception as e:
        print(f"Error deleting entry: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/api/update-entry/<entry_id>', methods=['PUT'])
@login_required
def update_entry(entry_id):
    try:
        data = request.get_json()
        college_id = session.get('college_id')
        
        # Verify ownership
        response = supabase.table('College_Course_Teaching_Details').select('*').eq('id', entry_id).execute()
        if not response.data or response.data[0]['College_id'] != college_id:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Prepare update data
        update_data = {
            'Teacher_Name': data.get('teacher_name'),
            'paper_name': data.get('paper_name'),
            'Semester': int(data.get('semester')),
            'Theory_Practical': data.get('theory_practical'),
            'Teacher_Status': data.get('teacher_status'),
            'Paper_type': data.get('paper_type'),
            'UPC_code': data.get('upc_code'),
        }
        
        # Update in Supabase
        supabase.table('College_Course_Teaching_Details').update(update_data).eq('id', entry_id).execute()
        
        return jsonify({'success': True, 'message': 'Entry updated successfully'}), 200
        
    except Exception as e:
        print(f"Error updating entry: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/programs')
@login_required
def get_programs():
    """Get all programs from College_Course_Program_Details"""
    try:
        response = supabase.table('College_Course_Program_Details').select('Program_id, Course_Program_name').execute()
        
        programs = []
        if response.data:
            programs = [{'id': item.get('Program_id'), 'name': item.get('Course_Program_name')} for item in response.data]
        
        print(f"Fetched {len(programs)} programs")
        return jsonify({'success': True, 'data': programs}), 200
        
    except Exception as e:
        print(f"Error fetching programs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
