#!/bin/bash

# Installation Script for TIC Login Application
# Run this script to automatically install dependencies and set up the project

echo "======================================"
echo "TIC Login Application - Setup Script"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) found"

# Create virtual environment (optional but recommended)
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env file and add your Supabase credentials:"
    echo "   SUPABASE_URL=https://your-project.supabase.co"
    echo "   SUPABASE_KEY=your-anon-key"
    echo "   FLASK_SECRET_KEY=your-secret-key"
else
    echo "✅ .env file found"
fi

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Supabase credentials"
echo "2. Run SCHEMA.sql in Supabase SQL Editor to create tables"
echo "3. Run: python app.py"
echo "4. Open: http://localhost:5000"
echo ""
echo "For detailed instructions, see QUICK_START.md"
