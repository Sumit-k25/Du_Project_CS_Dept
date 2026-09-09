@echo off
REM Installation Script for Windows
REM Run this script to automatically install dependencies

echo ======================================
echo TIC Login Application - Setup Script
echo ======================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit the .env file and add your Supabase credentials:
    echo    SUPABASE_URL=https://your-project.supabase.co
    echo    SUPABASE_KEY=your-anon-key
    echo    FLASK_SECRET_KEY=your-secret-key
) else (
    echo .env file found
)

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Edit .env file with your Supabase credentials
echo 2. Run SCHEMA.sql in Supabase SQL Editor to create tables
echo 3. Run: python app.py
echo 4. Open: http://localhost:5000
echo.
echo For detailed instructions, see QUICK_START.md
echo.
pause
