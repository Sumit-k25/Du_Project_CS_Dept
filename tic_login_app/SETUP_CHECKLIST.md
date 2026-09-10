# ✅ Setup Checklist

Use this checklist to track your setup progress.

## Pre-Setup
- [ ] Python 3.8+ installed and working
- [ ] Supabase account created
- [ ] Project browser open
- [ ] Terminal/Command Prompt ready

## Step 1: Get Supabase Credentials
- [ ] Go to Supabase dashboard
- [ ] Select project: DU_Computer_Science_initial
- [ ] Go to Settings → API
- [ ] Copy Project URL (SUPABASE_URL)
- [ ] Copy anon public key (SUPABASE_KEY)
- [ ] Have both credentials ready

## Step 2: Create .env File
- [ ] Navigate to `tic_login_app` folder
- [ ] Create file named `.env` (not `.env.txt`)
- [ ] Add SUPABASE_URL
- [ ] Add SUPABASE_KEY
- [ ] Add FLASK_SECRET_KEY (any random string)
- [ ] Add FLASK_ENV=development
- [ ] Save file

**Example .env:**
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
FLASK_SECRET_KEY=my-secret-key
FLASK_ENV=development
```

## Step 3: Install Dependencies
- [ ] Open terminal in `tic_login_app` folder
- [ ] Run: `pip install -r requirements.txt`
- [ ] Wait for all packages to install
- [ ] No errors should appear

**Packages Installed:**
- [ ] Flask (web framework)
- [ ] supabase (database client)
- [ ] python-dotenv (environment variables)
- [ ] requests (HTTP library)

## Step 4: Create Database Tables
- [ ] Go to Supabase dashboard
- [ ] Click SQL Editor
- [ ] Click New Query
- [ ] Open `SCHEMA.sql` file
- [ ] Copy all contents
- [ ] Paste into Supabase query editor
- [ ] Click Run
- [ ] Wait for success message
- [ ] Close query

**Tables Created:**
- [ ] College_Details
- [ ] Users
- [ ] Paper_Details
- [ ] Collage_Course_Program_Details
- [ ] Collage_Course_Teaching_Details

**Indexes Created:**
- [ ] idx_users_tic_mail
- [ ] idx_college_details_tic_email
- [ ] idx_teaching_details_college_id
- [ ] idx_teaching_details_semester
- [ ] idx_paper_details_semester

## Step 5: Add Test Data
- [ ] In Supabase SQL Editor, create new query
- [ ] Copy test data SQL:
```sql
INSERT INTO College_Details (College_Code, College_Name, Tic_Email)
VALUES (1, 'Delhi University - Computer Science', 'tic@du.edu.in');

INSERT INTO Users (tic_mail, password)
VALUES ('tic@du.edu.in', 'password123');
```
- [ ] Click Run
- [ ] Verify data inserted (2 rows)

## Step 6: Run Application
- [ ] Open terminal in `tic_login_app` folder
- [ ] Run: `python app.py` (or `python3 app.py` on Mac/Linux)
- [ ] You should see: "Running on http://localhost:5001"
- [ ] No errors in terminal
- [ ] Terminal shows "WARNING: This is a development server"

## Step 7: Access Application
- [ ] Open web browser (Chrome, Firefox, Safari, Edge)
- [ ] Go to: `http://localhost:5001`
- [ ] You should see login page
- [ ] Page loads without errors

## Step 8: Login Test
- [ ] Enter email: `tic@du.edu.in`
- [ ] Enter password: `password123`
- [ ] Click Login
- [ ] Should redirect to dashboard
- [ ] College name "Delhi University - Computer Science" appears

## Step 9: Test Features
### Add Entry
- [ ] Fill form fields
- [ ] Click "Add Entry"
- [ ] Success message appears
- [ ] Entry appears in table

### View Entries
- [ ] Table displays all entries
- [ ] Shows correct columns
- [ ] Data displays correctly

### Edit Entry
- [ ] Click Edit button
- [ ] Modal opens
- [ ] Fields populate
- [ ] Update values
- [ ] Click Update
- [ ] Changes appear in table

### Delete Entry
- [ ] Click Delete button
- [ ] Confirm dialog appears
- [ ] Entry removed from table
- [ ] Entry removed from database

## Step 10: Verify Installation
- [ ] All forms work without errors
- [ ] Database saves data correctly
- [ ] Grid displays all entries
- [ ] Edit functionality works
- [ ] Delete functionality works
- [ ] Logout works
- [ ] Can login again

## Troubleshooting Checklist

If something doesn't work:

### .env File Issues
- [ ] File named `.env` (not `.env.txt`)
- [ ] Located in `tic_login_app` folder
- [ ] Contains all 4 variables
- [ ] No missing values
- [ ] No extra spaces around `=`

### Installation Issues
- [ ] Python 3.8+ installed
- [ ] Run `pip install -r requirements.txt` again
- [ ] No syntax errors in output
- [ ] All 4 packages installed

### Database Issues
- [ ] Supabase project is active
- [ ] SCHEMA.sql ran without errors
- [ ] Tables exist in Supabase
- [ ] Test data inserted successfully
- [ ] Can see data in Supabase tables view

### Connection Issues
- [ ] Internet connection working
- [ ] SUPABASE_URL correct format
- [ ] SUPABASE_KEY copied correctly
- [ ] .env file values exact (no typos)

### Application Issues
- [ ] Flask started successfully
- [ ] No port conflicts (5001 available)
- [ ] Can access http://localhost:5001
- [ ] Login page loads
- [ ] JavaScript console shows no errors (F12)

## Success Indicators
✅ Application is ready when:
- [ ] You can login with test credentials
- [ ] Dashboard displays without errors
- [ ] You can add a new entry
- [ ] You can view all entries in grid
- [ ] You can edit an entry
- [ ] You can delete an entry
- [ ] All data persists after logout/login

---

## Common Issues Quick Fix

| Issue | Fix |
|-------|-----|
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| .env not found | Create .env file with credentials |
| Connection refused | Check SUPABASE_URL and KEY are correct |
| tic_mail column not found | Run SCHEMA.sql in Supabase |
| Login fails | Check password is exactly `password123` |
| Port 5001 in use | Stop the process using port 5001 or change the configured port in `app.py` |
| Table not found | Verify all tables created from SCHEMA.sql |

---

## Next Steps (Optional)
- [ ] Add more test colleges and users
- [ ] Customize login page styling
- [ ] Add export to Excel feature
- [ ] Set up email notifications
- [ ] Deploy to production
- [ ] Add user management
- [ ] Add advanced filtering
- [ ] Create admin panel

---

## Documentation Links
- 📖 [README.md](README.md) - Full documentation
- 🚀 [QUICK_START.md](QUICK_START.md) - Quick 7-step guide
- 📋 [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Complete setup guide
- 🏗️ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Architecture details
- ⚙️ [SETUP_GUIDE.py](SETUP_GUIDE.py) - Setup reference

---

## Support Resources
- **Python Docs**: https://docs.python.org/3/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Supabase Docs**: https://supabase.com/docs
- **Stack Overflow**: Tag your questions with `flask`, `supabase`

---

## Estimated Times
- Prerequisites check: 5 minutes
- Supabase setup: 5 minutes
- Installation: 5 minutes
- Database setup: 5 minutes
- Testing: 10 minutes
- **Total**: ~30 minutes

---

**Last Updated**: September 6, 2026  
**Version**: 1.0  
**Status**: Complete

Good luck! 🎉
