"""
Quick Setup Guide for Supabase Configuration
"""

# STEP 1: Get Supabase Credentials
# ================================
# 1. Go to https://supabase.com/
# 2. Sign in or create an account
# 3. Create a new project or use existing: "DU_Computer_Science_initial"
# 4. Go to Project Settings → API
# 5. Copy these values to .env file:
#    - Project URL → SUPABASE_URL
#    - anon public key → SUPABASE_KEY

# STEP 2: Create Database Tables
# ================================
# 1. In Supabase Dashboard, go to SQL Editor
# 2. Create a new query
# 3. Copy and paste the SQL schema from SCHEMA.sql file
# 4. Run the query

# STEP 3: Add Test Data (Optional)
# ================================
# Run this SQL to add test credentials:

"""
-- Add test college
INSERT INTO College_Details (College_Code, College_Name, Tic_Email)
VALUES (1, 'Delhi University - Computer Science', 'tic@du.edu.in')
ON CONFLICT (College_Code) DO NOTHING;

-- Add test user (Password: password123)
INSERT INTO Users (tic_mail, password)
VALUES ('tic@du.edu.in', 'password123')
ON CONFLICT (tic_mail) DO NOTHING;

-- Add test teaching details
INSERT INTO Collage_Course_Teaching_Details 
(College_id, Course_id, Semester, Paper_type, paper_name, UPC_code, Teacher_Name, Theory_Practical, Teacher_Status)
VALUES 
(1, 101, 1, 'Theory', 'Introduction to Programming', 'UPC001', 'Dr. John Doe', 'Theory', 'Permanent'),
(1, 102, 1, 'Practical', 'Programming Lab', 'UPC002', 'Prof. Jane Smith', 'Practical', 'Guest'),
(1, 103, 2, 'Theory', 'Data Structures', 'UPC003', 'Dr. Robert Brown', 'Theory', 'Adhoc');
"""

# STEP 4: Configure .env File
# ============================
# Update .env with your credentials:

"""
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
"""

# STEP 5: Install Dependencies
# =============================
# Run this command in your terminal:
# pip install -r requirements.txt

# STEP 6: Run Application
# =======================
# python app.py
# Then open: http://localhost:5000

print("Setup Guide - See comments in this file for step-by-step instructions")
