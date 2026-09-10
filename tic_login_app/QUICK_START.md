# 🚀 QUICK START GUIDE

## Step 1: Prerequisites
- Python 3.8+ installed
- pip package manager
- Supabase account

## Step 2: Install Dependencies

```bash
cd tic_login_app
pip install -r requirements.txt
```

## Step 3: Get Supabase Credentials

1. Go to [Supabase Dashboard](https://supabase.com/)
2. Sign in to your account
3. Select project: **DU_Computer_Science_initial**
4. Go to **Project Settings** (bottom left) → **API**
5. Copy the following:
   - **Project URL** → This is your `SUPABASE_URL`
   - **anon public key** → This is your `SUPABASE_KEY`

## Step 4: Configure .env File

1. Rename `.env.example` to `.env`
2. Add your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

## Step 5: Create Database Tables

1. Go to Supabase Dashboard
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy contents from `SCHEMA.sql` file
5. Click **Run**
6. Wait for successful completion

## Step 6: Add Test Data (Optional)

Run this SQL in Supabase SQL Editor:

```sql
-- Add test college
INSERT INTO College_Details (College_Code, College_Name, Tic_Email)
VALUES (1, 'Delhi University - Computer Science', 'tic@du.edu.in')
ON CONFLICT (College_Code) DO NOTHING;

-- Add test user
INSERT INTO Users (tic_mail, password)
VALUES ('tic@du.edu.in', 'password123')
ON CONFLICT (tic_mail) DO NOTHING;
```

## Step 7: Run the Application

```bash
python app.py
```

## Step 8: Access the Application

1. Open your browser
2. Go to: **http://localhost:5001**
3. Login with:
   - Email: `tic@du.edu.in`
   - Password: `password123`

## 🎉 You're Done!

The dashboard should load and you can start adding course paper details.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'supabase'"
**Solution**: Run `pip install -r requirements.txt` again

### Issue: "SUPABASE_URL not found in environment"
**Solution**: Check your `.env` file exists and has correct values

### Issue: "Connection refused"
**Solution**: 
- Check internet connection
- Verify Supabase project is active
- Check SUPABASE_URL and KEY are correct

### Issue: "tic_mail column not found"
**Solution**: Run SCHEMA.sql in Supabase to create tables

### Issue: "Login failed"
**Solution**: 
- Ensure test data is inserted correctly
- Check if column name is `tic_mail` (not `tic_email`)
- Verify password is exactly `password123`

---

## Next Steps

1. Add more colleges and users
2. Add course paper details
3. Customize styling in `static/css/style.css`
4. Add more features as needed

---

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [SETUP_GUIDE.py](SETUP_GUIDE.py) for additional setup info
- Check browser console for JavaScript errors (F12)
- Check Flask terminal output for backend errors

---

**Database Name**: DU_Computer_Science_initial  
**Database Password**: Jeesu@192113920

Happy coding! 🎓
