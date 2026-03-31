#!/bin/bash
# Activation script for Linux/Mac
echo "🚀 Activating IoT Alert Dashboard Backend Environment"
echo "====================================================="

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 setup_venv.py"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Show status
echo "✅ Virtual environment activated!"
echo "📁 Current directory: $(pwd)"
echo "🐍 Python version:"
python --version
echo "📦 Pip version:"
pip --version

echo ""
echo "📋 Available commands:"
echo "  python main.py              - Start the FastAPI server"
echo "  python verify_supabase.py   - Test database connection"
echo "  python test_db_connection.py - Test database setup"
echo "  pip list                    - Show installed packages"
echo "  deactivate                  - Exit virtual environment"
echo ""

# Start a new shell with the activated environment
exec $SHELL