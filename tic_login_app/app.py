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
        if not course_id:
            return jsonify({'success': False, 'message': 'Please select a program/course'}), 400

        # Course_id must be a valid Program_id from College_Course_Program_Details.
        program_response = (
            supabase.table('College_Course_Program_Details')
            .select('Program_id')
            .eq('Program_id', int(course_id))
            .execute()
        )
        if not program_response.data:
            return jsonify({'success': False, 'message': 'Selected program/course is invalid'}), 400

        paper_id = data.get('paper_id')
        if not paper_id:
            return jsonify({'success': False, 'message': 'Please select a paper name'}), 400

        paper_master = (
            supabase.table('Paper_Details')
            .select('paper_id, Paper_Name, UPC_Code')
            .eq('program_id', int(course_id))
            .eq('paper_id', int(paper_id))
            .execute()
        )
        if not paper_master.data:
            return jsonify({'success': False, 'message': 'Selected paper is invalid for this course'}), 400

        entry_data = {
            'College_id': college_id,
            'Course_id': int(course_id),
            'Semester': int(data.get('semester')),
            'Paper_type': data.get('paper_type'),
            'paper_id': int(paper_id),
            'UPC_code': data.get('upc_code') or paper_master.data[0].get('UPC_Code'),
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

def _resolve_paper_name_from_legacy_id(course_id, value):
    if value is None:
        return value

    try:
        numeric_value = int(str(value).strip())
    except (TypeError, ValueError):
        return value

    try:
        response = (
            supabase.table('Paper_Details')
            .select('*')
            .eq('program_id', int(course_id))
            .eq('paper_id', numeric_value)
            .execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0].get('Paper_Name') or value
    except Exception as e:
        print(f"Error resolving legacy paper name: {str(e)}")

    return value


def _resolve_paper_name_for_entry(entry):
    course_id = entry.get('Course_id')
    paper_id = entry.get('paper_id')
    paper_name = entry.get('paper_name')

    if paper_id is not None:
        try:
            response = (
                supabase.table('Paper_Details')
                .select('Paper_Name')
                .eq('program_id', int(course_id))
                .eq('paper_id', int(paper_id))
                .execute()
            )
            if response.data and len(response.data) > 0:
                return response.data[0].get('Paper_Name')
        except Exception as e:
            print(f"Error resolving paper name for entry: {str(e)}")

    if paper_name is not None:
        return _resolve_paper_name_from_legacy_id(course_id, paper_name)

    return None


@app.route('/api/entries/<college_id>')
@login_required
def get_entries(college_id):
    try:
        if int(college_id) != session.get('college_id'):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403

        response = supabase.table('College_Course_Teaching_Details').select('*').eq('College_id', college_id).execute()
        entries = response.data if response.data else []

        for entry in entries:
            resolved_name = _resolve_paper_name_for_entry(entry)
            if resolved_name is not None:
                entry['paper_name'] = resolved_name

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
        
        paper_id = data.get('paper_id')
        if not paper_id:
            return jsonify({'success': False, 'message': 'Please select a paper name'}), 400

        paper_master = (
            supabase.table('Paper_Details')
            .select('paper_id, UPC_Code')
            .eq('program_id', int(response.data[0].get('Course_id')))
            .eq('paper_id', int(paper_id))
            .execute()
        )
        if not paper_master.data:
            return jsonify({'success': False, 'message': 'Selected paper is invalid for this course'}), 400

        update_data = {
            'Teacher_Name': data.get('teacher_name'),
            'paper_id': int(paper_id),
            'Semester': int(data.get('semester')),
            'Theory_Practical': data.get('theory_practical'),
            'Teacher_Status': data.get('teacher_status'),
            'Paper_type': data.get('paper_type'),
            'UPC_code': data.get('upc_code') or paper_master.data[0].get('UPC_Code'),
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

def _first_available_value(record, *keys):
    for key in keys:
        if key in record and record.get(key) is not None:
            return record.get(key)
    return None


def _get_paper_records(course_id=None, semester=None, paper_type=None):
    try:
        response = supabase.table('Paper_Details').select('*').execute()
        records = response.data or []
    except Exception as e:
        print(f"Error fetching paper details: {str(e)}")
        return []

    filtered = []
    for record in records:
        program_value = _first_available_value(record, 'program_id', 'Program_id', 'Course_id', 'course_id', 'Course_Id')
        semester_value = _first_available_value(record, 'Semester', 'semester')
        paper_type_value = _first_available_value(record, 'Paper_type', 'paper_type', 'Paper_Type')

        if course_id is not None and course_id != '' and program_value is not None and str(program_value) != str(course_id):
            continue
        if semester is not None and semester != '' and semester_value is not None and str(semester_value) != str(semester):
            continue
        if paper_type is not None and paper_type != '' and paper_type_value is not None and str(paper_type_value).strip().lower() != str(paper_type).strip().lower():
            continue
        filtered.append(record)

    return filtered


@app.route('/api/programs')
@login_required
def get_programs():
    """Get all programs from College_Course_Program_Details"""
    try:
        response = (
            supabase.table('College_Course_Program_Details')
            .select('Program_id, Course_Program_name')
            .order('Course_Program_name')
            .execute()
        )
        
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


@app.route('/api/paper-semesters')
@login_required
def get_paper_semesters():
    try:
        course_id = request.args.get('course_id')
        records = _get_paper_records(course_id=course_id)
        semesters = []

        for record in records:
            value = _first_available_value(record, 'Semester', 'semester')
            if value is not None:
                semesters.append(int(value))

        unique_semesters = sorted(set(semesters))
        data = [{'id': semester, 'name': f'Semester {semester}'} for semester in unique_semesters]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        print(f"Error fetching paper semesters: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/paper-types')
@login_required
def get_paper_types():
    try:
        course_id = request.args.get('course_id')
        semester = request.args.get('semester')
        records = _get_paper_records(course_id=course_id, semester=semester)

        paper_types = []
        for record in records:
            value = _first_available_value(record, 'Paper_type', 'paper_type', 'Paper_Type')
            if value is not None:
                paper_types.append(str(value).strip())

        unique_types = []
        for paper_type in paper_types:
            if paper_type not in unique_types:
                unique_types.append(paper_type)

        data = [{'id': paper_type, 'name': paper_type} for paper_type in unique_types]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        print(f"Error fetching paper types: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/paper-names')
@login_required
def get_paper_names():
    try:
        course_id = request.args.get('course_id')
        semester = request.args.get('semester')
        paper_type = request.args.get('paper_type')
        records = _get_paper_records(course_id=course_id, semester=semester, paper_type=paper_type)

        paper_names = []
        for record in records:
            name = _first_available_value(record, 'Paper_Name', 'paper_name', 'PaperName', 'Paper Name')
            upc = _first_available_value(record, 'UPC_Code', 'UPC_code', 'upc_code', 'UPC Code')
            paper_id = _first_available_value(record, 'paper_id', 'Paper_id', 'Paper_ID')
            if name is not None:
                paper_names.append({
                    'id': str(paper_id).strip() if paper_id is not None else str(name).strip(),
                    'paper_id': str(paper_id).strip() if paper_id is not None else str(name).strip(),
                    'name': str(name).strip(),
                    'upc_code': str(upc).strip() if upc is not None else ''
                })

        unique_names = []
        seen = set()
        for paper in paper_names:
            key = paper['id']
            if key not in seen:
                seen.add(key)
                unique_names.append(paper)

        return jsonify({'success': True, 'data': unique_names}), 200
    except Exception as e:
        print(f"Error fetching paper names: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
