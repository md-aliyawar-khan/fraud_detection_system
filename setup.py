#!/usr/bin/env python3
"""
Setup script for Fraud Detection System
This script helps users set up and run the fraud detection system.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print a welcome banner"""
    print("=" * 60)
    print("FRAUD DETECTION SYSTEM SETUP")
    print("=" * 60)
    print("This script will help you set up the fraud detection system.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def check_data_files():
    """Check if required data files exist"""
    print("\nChecking data files...")
    
    required_files = [
        "data/raw/creditcard_2023.csv",
        "models/fraud_detection_model.pkl",
        "models/scaler.pkl"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"{file_path}")
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        print("You need to run the data pipeline first.")
        return False
    
    return True

def run_data_pipeline():
    """Run the data preprocessing and training pipeline"""
    print("\nRunning data pipeline...")
    
    scripts = [
        "scripts/preprocess.py",
        "scripts/train.py"
    ]
    
    for script in scripts:
        print(f"Running {script}...")
        try:
            subprocess.check_call([sys.executable, script])
            print(f"{script} completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")
            return False
    
    return True

def test_api():
    """Test the API functionality"""
    print("\nTesting API...")
    try:
        subprocess.check_call([sys.executable, "test_api.py"])
        print("API tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"API tests failed: {e}")
        return False

def start_server():
    """Start the Flask development server"""
    print("\nStarting Flask server...")
    print("The web interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nServer stopped.")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Check if data pipeline needs to be run
    if not check_data_files():
        print("\nData files missing. Running data pipeline...")
        if not run_data_pipeline():
            print("Data pipeline failed. Please check the error messages above.")
            sys.exit(1)
    
    # Test API
    if not test_api():
        print("API tests failed. Please check the error messages above.")
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python app.py' to start the server")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Use the web interface to test fraud detection")
    print("4. For API usage, see README.md for examples")
    
    # Ask if user wants to start the server
    response = input("\nWould you like to start the server now? (y/n): ").lower()
    if response in ['y', 'yes']:
        start_server()

if __name__ == "__main__":
    main() 