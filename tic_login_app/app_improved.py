"""
Improved Flask Application with Database Integration
TIC Login & Course Paper Management System
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from supabase import create_client, Client
from config import get_config
from database import DatabaseHelper
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(get_config())

# Initialize Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
db = DatabaseHelper(supabase)

# ============= DECORATORS =============

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tic_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============= ROUTES =============

@app.route('/')
def index():
    """Home page - redirect to dashboard or login"""
    if 'tic_email' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        data = request.get_json()
        tic_email = data.get('tic_email', '').strip()
        password = data.get('password', '')

        if not tic_email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400

        try:
            # Authenticate user
            user = db.authenticate_user(tic_email, password)
            
            if user:
                # Get college details
                college = db.get_college_by_tic_email(tic_email)
                
                if college:
                    session['tic_email'] = tic_email
                    session['college_id'] = college['College_Code']
                    session['college_name'] = college['College_Name']
                    session.permanent = True
                    
                    return jsonify({'success': True, 'message': 'Login successful'}), 200
                else:
                    return jsonify({'success': False, 'message': 'College information not found'}), 401
            else:
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({'success': False, 'message': 'An error occurred during login'}), 500

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    try:
        college_id = session.get('college_id')
        college_name = session.get('college_name')
        
        # Fetch all teaching details for this college
        entries = db.get_teaching_details_by_college(college_id)
        
        return render_template('dashboard.html', 
                             college_name=college_name,
                             entries=entries)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return render_template('dashboard.html', 
                             college_name=session.get('college_name'),
                             entries=[],
                             error="Failed to load entries")

@app.route('/api/add-entry', methods=['POST'])
@login_required
def add_entry():
    """Add new course teaching detail"""
    try:
        data = request.get_json()
        college_id = session.get('college_id')
        
        # Validate required fields
        required_fields = ['course_id', 'semester', 'paper_type', 'paper_name', 
                          'upc_code', 'teacher_name', 'theory_practical', 'teacher_status']
        
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Prepare data for insertion
        entry_data = {
            'College_id': college_id,
            'Course_id': int(data.get('course_id')),
            'Semester': int(data.get('semester')),
            'Paper_type': data.get('paper_type'),
            'paper_name': data.get('paper_name'),
            'UPC_code': data.get('upc_code'),
            'Teacher_Name': data.get('teacher_name'),
            'Theory_Practical': data.get('theory_practical'),
            'Teacher_Status': data.get('teacher_status'),
        }
        
        # Insert into database
        result = db.add_teaching_detail(entry_data)
        
        if result:
            return jsonify({
                'success': True, 
                'message': 'Entry added successfully', 
                'data': result
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to add entry'}), 400
            
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        print(f"Error adding entry: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/entries/<college_id>')
@login_required
def get_entries(college_id):
    """Get all entries for a specific college"""
    try:
        # Verify user belongs to this college
        if int(college_id) != session.get('college_id'):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        entries = db.get_teaching_details_by_college(int(college_id))
        
        return jsonify({'success': True, 'data': entries}), 200
        
    except Exception as e:
        print(f"Error fetching entries: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to fetch entries'}), 500

@app.route('/api/update-entry/<entry_id>', methods=['PUT'])
@login_required
def update_entry(entry_id):
    """Update an existing course teaching detail"""
    try:
        data = request.get_json()
        college_id = session.get('college_id')
        
        # Verify ownership
        entry = db.get_teaching_detail_by_id(int(entry_id))
        if not entry or entry['College_id'] != college_id:
            return jsonify({'success': False, 'message': 'Unauthorized or entry not found'}), 403
        
        # Prepare update data
        update_data = {
            'Teacher_Name': data.get('teacher_name', entry['Teacher_Name']),
            'paper_name': data.get('paper_name', entry['paper_name']),
            'Semester': int(data.get('semester', entry['Semester'])),
            'Theory_Practical': data.get('theory_practical', entry['Theory_Practical']),
            'Teacher_Status': data.get('teacher_status', entry['Teacher_Status']),
            'Paper_type': data.get('paper_type', entry['Paper_type']),
            'UPC_code': data.get('upc_code', entry['UPC_code']),
        }
        
        # Update in database
        success = db.update_teaching_detail(int(entry_id), update_data)
        
        if success:
            return jsonify({'success': True, 'message': 'Entry updated successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to update entry'}), 400
        
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        print(f"Error updating entry: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/delete-entry/<entry_id>', methods=['DELETE'])
@login_required
def delete_entry(entry_id):
    """Delete a course teaching detail"""
    try:
        college_id = session.get('college_id')
        
        # Verify ownership
        entry = db.get_teaching_detail_by_id(int(entry_id))
        if not entry or entry['College_id'] != college_id:
            return jsonify({'success': False, 'message': 'Unauthorized or entry not found'}), 403
        
        # Delete the entry
        success = db.delete_teaching_detail(int(entry_id))
        
        if success:
            return jsonify({'success': True, 'message': 'Entry deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to delete entry'}), 400
        
    except Exception as e:
        print(f"Error deleting entry: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/search-entries', methods=['POST'])
@login_required
def search_entries():
    """Search entries by teacher name or paper name"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '').strip()
        college_id = session.get('college_id')
        
        if not search_term:
            return jsonify({'success': False, 'message': 'Search term is required'}), 400
        
        entries = db.search_teaching_details(college_id, search_term)
        
        return jsonify({'success': True, 'data': entries}), 200
        
    except Exception as e:
        print(f"Error searching entries: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    print(f"Server error: {str(error)}")
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

# ============= MAIN =============

if __name__ == '__main__':
    app.run(
        debug=app.config.get('DEBUG', True),
        host='0.0.0.0',
        port=5000
    )
