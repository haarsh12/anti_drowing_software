#!/usr/bin/env python3
"""
Virtual Environment Setup Script for IoT Alert Dashboard Backend
"""
import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """Set up virtual environment and install dependencies"""
    print("🚀 Setting up IoT Alert Dashboard Backend Environment")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Get the current directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(backend_dir, "venv")
    
    print(f"📁 Backend directory: {backend_dir}")
    print(f"📁 Virtual environment path: {venv_path}")
    
    # Remove existing venv if it exists
    if os.path.exists(venv_path):
        print("🗑️ Removing existing virtual environment...")
        if platform.system() == "Windows":
            run_command(f'rmdir /s /q "{venv_path}"', "Removing old venv")
        else:
            run_command(f'rm -rf "{venv_path}"', "Removing old venv")
    
    # Create virtual environment
    if not run_command(f'python -m venv "{venv_path}"', "Creating virtual environment"):
        return False
    
    # Determine activation script path
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    # Upgrade pip
    if not run_command(f'"{python_path}" -m pip install --upgrade pip', "Upgrading pip"):
        return False
    
    # Install requirements
    requirements_path = os.path.join(backend_dir, "requirements.txt")
    if not os.path.exists(requirements_path):
        print("❌ requirements.txt not found")
        return False
    
    if not run_command(f'"{pip_path}" install -r "{requirements_path}"', "Installing dependencies"):
        return False
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    result = run_command(f'"{pip_path}" list', "Listing installed packages")
    if result:
        print("📦 Installed packages:")
        for line in result.split('\n')[:10]:  # Show first 10 packages
            if line.strip():
                print(f"   {line}")
        if len(result.split('\n')) > 10:
            print("   ... and more")
    
    print("\n" + "=" * 60)
    print("🎉 Virtual environment setup completed successfully!")
    print("\n📋 Next steps:")
    
    if platform.system() == "Windows":
        print(f"1. Activate the environment:")
        print(f"   {activate_script}")
        print(f"2. Or use the batch file:")
        print(f"   activate_venv.bat")
    else:
        print(f"1. Activate the environment:")
        print(f"   source {activate_script}")
        print(f"2. Or use the shell script:")
        print(f"   ./activate_venv.sh")
    
    print(f"3. Run the server:")
    print(f"   python main.py")
    print(f"4. Test the API:")
    print(f"   python verify_supabase.py")
    
    return True

if __name__ == "__main__":
    success = setup_virtual_environment()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)