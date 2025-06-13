#!/bin/bash

# Morse Code Translator Web Application Startup Script
# This script starts both the backend API server and frontend development server

set -e  # Exit on any error

echo "🚀 Starting Morse Code Translator Web Application..."
echo "=================================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo "✅ Cleanup complete"
    exit 0
}

# Set up cleanup trap
trap cleanup SIGINT SIGTERM

# Check for required commands
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Error: python3 is not installed or not in PATH"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ Error: npm is not installed or not in PATH"
    exit 1
fi

if ! command_exists pip3; then
    echo "❌ Error: pip3 is not installed or not in PATH"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Check if ports are available
echo "🔍 Checking port availability..."

if port_in_use 8000; then
    echo "⚠️  Warning: Port 8000 is already in use (backend)"
    echo "   The backend server might already be running"
fi

if port_in_use 3000; then
    echo "⚠️  Warning: Port 3000 is already in use (frontend)"
    echo "   The frontend server might already be running"
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

echo "   Activating virtual environment..."
source venv/bin/activate

echo "   Installing Python packages..."
pip3 install -r requirements.txt

echo "✅ Backend dependencies installed"

# Start backend server
echo "🔧 Starting backend server..."
cd app
python3 main.py &
BACKEND_PID=$!
cd ../..

# Wait a moment for backend to start
sleep 3

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing npm packages..."
    npm install
else
    echo "   npm packages already installed"
fi

echo "✅ Frontend dependencies ready"

# Start frontend server
echo "🔧 Starting frontend development server..."
npm start &
FRONTEND_PID=$!
cd ..

# Wait for servers to start
echo "⏳ Waiting for servers to start..."
sleep 5

echo ""
echo "🎉 Morse Code Translator is now running!"
echo "=================================================="
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Keep script running and wait for user to stop
wait
