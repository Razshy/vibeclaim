#!/usr/bin/env python3
"""
Setup and run script for Windsurf Credit Claimer
This script will install dependencies and run the automation.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def check_chrome_driver():
    """Check if Chrome is available."""
    try:
        subprocess.run(["google-chrome", "--version"], capture_output=True, check=True)
        print("Chrome browser found!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["chromium-browser", "--version"], capture_output=True, check=True)
            print("Chromium browser found!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Chrome/Chromium browser not found. Please install Google Chrome.")
            return False

def main():
    """Main setup and run function."""
    print("=== Windsurf Credit Claimer Setup ===")
    
    # Check if we're in the right directory
    if not os.path.exists("windsurf_credit_claimer.py"):
        print("Error: windsurf_credit_claimer.py not found in current directory")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check Chrome
    if not check_chrome_driver():
        print("Please install Google Chrome and try again.")
        return
    
    print("\n=== Setup Complete! ===")
    print("Running Windsurf Credit Claimer...")
    
    # Run the main script
    try:
        subprocess.run([sys.executable, "windsurf_credit_claimer.py"])
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Error running script: {e}")

if __name__ == "__main__":
    main()
