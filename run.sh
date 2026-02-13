#!/bin/bash

# Student Management System - Startup Script

echo "=========================================="
echo "Student Management System"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run the application
echo ""
echo "=========================================="
echo "🚀 Starting Student Management System"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  🌐 http://localhost:5001"
echo ""
echo "Sample Credentials:"
echo "  Faculty: EMP001 / faculty123"
echo "  Student: 20240101"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 app.py
