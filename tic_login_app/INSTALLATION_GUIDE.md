# Complete Installation & Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [Supabase Configuration](#supabase-configuration)
5. [Running the Application](#running-the-application)
6. [Features & Usage](#features--usage)
7. [Troubleshooting](#troubleshooting)
8. [API Reference](#api-reference)

---

## Prerequisites

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** - [Download](https://git-scm.com/downloads) (optional)
- **Modern Web Browser** - Chrome, Firefox, Safari, Edge

### Required Accounts
- **Supabase Account** - [Sign up free](https://supabase.com/)
- **Database** - `DU_Computer_Science_initial`

### System Requirements
- 50MB free disk space
- 2GB RAM minimum
- Internet connection

---

## Project Structure

```
tic_login_app/
├── app.py                      # Main Flask application (original)
├── app_improved.py             # Improved Flask app with better structure
├── config.py                   # Configuration management
├── database.py                 # Database helper functions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (CREATE THIS)
├── .env.example                # Example environment file
├── SCHEMA.sql                  # Database schema SQL
├── QUICK_START.md              # Quick start guide
├── README.md                   # Full documentation
├── SETUP_GUIDE.py              # Setup instructions
├── install.sh                  # Linux/Mac installation script
├── install.bat                 # Windows installation script
├── templates/
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   └── dashboard.html         # Main dashboard
└── static/
    ├── css/
    │   └── style.css          # Styling
    └── js/
        └── script.js          # JavaScript utilities
```

---

## Step-by-Step Installation

### Step 1: Create .env File

**On Windows:**
1. Open Notepad
2. Paste the following content:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
FLASK_SECRET_KEY=dev-secret-key
FLASK_ENV=development
```

3. Save as `.env` (not `.env.txt`) in the `tic_login_app` folder

**On Mac/Linux:**
```bash
cd tic_login_app
cat > .env << EOF
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
FLASK_SECRET_KEY=dev-secret-key
FLASK_ENV=development
EOF
```

### Step 2: Install Python Dependencies

**On Windows:**
```bash
cd tic_login_app
pip install -r requirements.txt
```

**On Mac/Linux:**
```bash
cd tic_login_app
python3 -m pip install -r requirements.txt
```

Or use the automatic script:
```bash
# Mac/Linux
bash install.sh

# Windows
install.bat
```

### Step 3: Get Supabase Credentials

1. Go to https://supabase.com/
2. Sign in with your account
3. Select your project: **DU_Computer_Science_initial**
4. Click **Settings** (bottom left)
5. Click **API**
6. Copy the **Project URL** (e.g., `https://xxxxx.supabase.co`)
7. Copy the **anon public key**
8. Paste these into your `.env` file

### Step 4: Set Up Database

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Open `SCHEMA.sql` file from the project
4. Copy all contents
5. Paste into Supabase SQL Editor
6. Click **Run**
7. Wait for success message

### Step 5: Add Test Data

In Supabase SQL Editor, create a new query and run:

```sql
-- Insert test college
INSERT INTO College_Details (College_Code, College_Name, Tic_Email)
VALUES (1, 'Delhi University - Computer Science', 'tic@du.edu.in')
ON CONFLICT (College_Code) DO NOTHING;

-- Insert test user
INSERT INTO Users (tic_mail, password)
VALUES ('tic@du.edu.in', 'password123')
ON CONFLICT (tic_mail) DO NOTHING;

-- Insert sample teaching details
INSERT INTO Collage_Course_Teaching_Details 
(College_id, Course_id, Semester, Paper_type, paper_name, UPC_code, Teacher_Name, Theory_Practical, Teacher_Status)
VALUES 
(1, 101, 1, 'Core', 'Introduction to Programming', 'UPC001', 'Dr. John Smith', 'Theory', 'Permanent'),
(1, 102, 1, 'Practical', 'Programming Lab', 'UPC002', 'Prof. Jane Doe', 'Practical', 'Guest'),
(1, 103, 2, 'Core', 'Data Structures', 'UPC003', 'Dr. Robert Brown', 'Both', 'Adhoc');
```

---

## Supabase Configuration

### Getting Your Credentials

**Project URL (SUPABASE_URL):**
- Format: `https://xxxxx.supabase.co`
- Found in: Settings → API → Project URL
- Example: `https://abcdef123456.supabase.co`

**Anon Public Key (SUPABASE_KEY):**
- Found in: Settings → API → anon public
- Format: Long alphanumeric string
- Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Database Details

- **Database Name**: DU_Computer_Science_initial
- **Database Password**: Jeesu@192113920
- **Host**: Provided by Supabase
- **Port**: 5432 (default PostgreSQL)

### Row-Level Security (Optional - Advanced)

For production, enable RLS in Supabase:

```sql
ALTER TABLE public.Users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.College_Details ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.Collage_Course_Teaching_Details ENABLE ROW LEVEL SECURITY;
```

---

## Running the Application

### Method 1: Direct Python

**Windows:**
```bash
cd tic_login_app
python app.py
```

**Mac/Linux:**
```bash
cd tic_login_app
python3 app.py
```

### Method 2: Using Improved App (Recommended)

**Windows:**
```bash
python app_improved.py
```

**Mac/Linux:**
```bash
python3 app_improved.py
```

### Access the Application

1. Open your browser
2. Go to: `http://localhost:5000`
3. You should see the login page

### Login Credentials (Test User)

- **Email**: `tic@du.edu.in`
- **Password**: `password123`

---

## Features & Usage

### Login Page
- Enter TIC email and password
- Click Login
- Redirects to dashboard on success

### Dashboard Features

#### 1. Add Course Paper Details
- **Teacher Name**: Full name of teacher
- **Paper Name**: Name of course/paper
- **Semester**: Select from 1-6
- **Theory/Practical**: Theory, Practical, or Both
- **Teacher Status**: Guest, Adhoc, or Permanent
- **UPC Code**: Unique paper identifier
- **Paper Type**: Course type (Core, Elective, etc.)
- **Course ID**: Course number

#### 2. View Entries
- Grid table displays all entries
- Shows: ID, Teacher, Paper, Semester, Type, Status, UPC, Actions
- Sortable columns
- Responsive design

#### 3. Edit Entry
- Click Edit button in table
- Modal dialog opens
- Update fields
- Click Update to save

#### 4. Delete Entry
- Click Delete button
- Confirm deletion
- Entry removed from database

### College-Specific Access
- Each TIC can only view/edit entries from their college
- College name shown in navbar
- All operations filtered by college_id

---

## Troubleshooting

### Installation Issues

**Problem: "ModuleNotFoundError: No module named 'supabase'"**
```bash
# Solution
pip install -r requirements.txt
# or
pip install supabase
```

**Problem: "No such file or directory: '.env'"**
```
Solution: Create .env file in tic_login_app folder
Copy .env.example and rename to .env
Add your Supabase credentials
```

### Connection Issues

**Problem: "Connection refused"**
- Check internet connection
- Verify Supabase project is active
- Confirm SUPABASE_URL is correct
- Check firewall settings

**Problem: "Invalid credentials"**
- Verify SUPABASE_URL format (must have https://)
- Verify SUPABASE_KEY is correct
- Check for trailing spaces in .env

### Database Issues

**Problem: "relation 'Collage_Course_Teaching_Details' does not exist"**
```
Solution:
1. Go to Supabase SQL Editor
2. Run SCHEMA.sql to create tables
3. Refresh page
```

**Problem: "column 'tic_mail' doesn't exist"**
```
Solution:
1. Check column name is lowercase: tic_mail (not tic_email)
2. Verify schema was run correctly
3. Check table exists: SELECT * FROM Users;
```

**Problem: "Login failed but credentials look correct"**
```
Solution:
1. Run: SELECT * FROM Users; in Supabase
2. Verify email is exactly: tic@du.edu.in
3. Verify password is exactly: password123
4. Check for extra spaces or special characters
```

### Application Issues

**Problem: "ModuleNotFoundError" for flask_cors or other packages**
```bash
pip install Flask flask-cors python-dotenv requests
```

**Problem: "Address already in use"**
```bash
# Port 5000 is busy, use different port
python app.py --port 5001
# or kill the process using port 5000
```

**Problem: "Session expires after page refresh"**
```
Solution:
1. Verify FLASK_SECRET_KEY is set in .env
2. Add: export FLASK_PERMANENT_SESSION_LIFETIME=3600
```

---

## API Reference

### Authentication Endpoints

**POST /login**
```json
Request:
{
  "tic_email": "tic@du.edu.in",
  "password": "password123"
}

Response (Success):
{
  "success": true,
  "message": "Login successful"
}

Response (Error):
{
  "success": false,
  "message": "Invalid email or password"
}
```

**GET /logout**
- Clears session
- Redirects to login

### Dashboard Endpoints

**GET /dashboard**
- Returns dashboard page
- Requires login
- Shows college name and entries

### Data Endpoints

**POST /api/add-entry**
```json
Request:
{
  "teacher_name": "Dr. John Smith",
  "paper_name": "Introduction to CS",
  "semester": "1",
  "theory_practical": "Theory",
  "teacher_status": "Permanent",
  "upc_code": "UPC001",
  "paper_type": "Core",
  "course_id": "101"
}

Response:
{
  "success": true,
  "message": "Entry added successfully",
  "data": { ...entry object... }
}
```

**GET /api/entries/<college_id>**
- Returns all entries for college
- Required: Login session
- Parameter: college_id

**PUT /api/update-entry/<entry_id>**
```json
Request: {
  "teacher_name": "Updated Name",
  "semester": "2",
  ...
}

Response:
{
  "success": true,
  "message": "Entry updated successfully"
}
```

**DELETE /api/delete-entry/<entry_id>**
- Deletes entry
- Returns success/failure

**POST /api/search-entries**
```json
Request:
{
  "search_term": "Dr. Smith"
}

Response:
{
  "success": true,
  "data": [ ...matching entries... ]
}
```

---

## Performance Tips

1. **Use Indexes**: Already included in SCHEMA.sql
2. **Limit Results**: Only load entries for logged-in college
3. **Compress CSS/JS**: Minify for production
4. **Cache Data**: Use browser caching headers
5. **Database Connection Pooling**: For multiple users

---

## Security Recommendations

⚠️ **For Production:**

1. **Password Hashing**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash passwords
hashed = generate_password_hash(password)

# Check passwords
check_password_hash(hashed, password)
```

2. **HTTPS**: Use SSL/TLS certificates
3. **CSRF Protection**: Add Flask-WTF
4. **Rate Limiting**: Use Flask-Limiter
5. **Input Validation**: Sanitize all inputs
6. **SQL Injection Prevention**: Use parameterized queries (already done)

---

## Deployment Guide

### Heroku Deployment

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SUPABASE_URL=...
heroku config:set SUPABASE_KEY=...
heroku config:set FLASK_SECRET_KEY=...

# Deploy
git push heroku main
```

### AWS Deployment

```bash
# Use Elastic Beanstalk
eb create tic-login-env
eb deploy
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## Support & Maintenance

### Regular Maintenance
- Back up database weekly
- Monitor error logs daily
- Update dependencies monthly
- Test login weekly

### Contact & Support
- Email: admin@du.edu.in
- Issues: GitHub Issues
- Documentation: See README.md

---

## Version History

- **v1.0** - Initial release with basic features
- **v1.1** - Added search functionality and improved UI
- **v2.0** - Added app_improved.py with better structure

---

**Last Updated**: September 6, 2026  
**Database**: DU_Computer_Science_initial  
**Status**: Production Ready
