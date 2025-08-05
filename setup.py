#!/usr/bin/env python3
"""
Setup script for the Slack Prayer Reminder Bot.
This script helps users configure the bot for first-time use.
"""

import os
import sys

def create_env_file():
    """Create a .env file template if it doesn't exist."""
    env_file = ".env"
    
    if os.path.exists(env_file):
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    print("Creating .env file template...")
    
    env_content = """# --- SECRETS ---
# Replace with your actual API keys
GEMINI_API_KEY="AIzaSy...YOUR_GEMINI_KEY"
SLACK_BOT_TOKEN="xoxb-...YOUR_SLACK_TOKEN"
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file template")
    print("📝 Please edit .env file with your actual API keys")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    required_packages = [
        'requests',
        'schedule', 
        'google-generativeai',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_data_files():
    """Check if Quran data files exist."""
    print("\nChecking data files...")
    
    required_files = [
        'data/quran.json',
        'data/ur.json'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing data files: {', '.join(missing_files)}")
        print("Please ensure Quran data files are in the data/ directory")
        return False
    
    print("✅ All data files present")
    return True

def run_test():
    """Run the test script to verify everything works."""
    print("\nRunning system test...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'test_new_bot.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ System test passed")
            return True
        else:
            print("❌ System test failed")
            print("Error output:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Could not run test: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Slack Prayer Reminder Bot Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    create_env_file()
    
    # Step 2: Check dependencies
    deps_ok = check_dependencies()
    
    # Step 3: Check data files
    data_ok = check_data_files()
    
    # Step 4: Run test (only if dependencies and data are ok)
    test_ok = False
    if deps_ok and data_ok:
        test_ok = run_test()
    
    # Summary
    print("\n" + "=" * 50)
    print("Setup Summary:")
    print(f"✅ Environment file: {'Created' if os.path.exists('.env') else 'Missing'}")
    print(f"✅ Dependencies: {'Installed' if deps_ok else 'Missing'}")
    print(f"✅ Data files: {'Present' if data_ok else 'Missing'}")
    print(f"✅ System test: {'Passed' if test_ok else 'Failed'}")
    
    if test_ok:
        print("\n🎉 Setup complete! Your bot is ready to run.")
        print("\nNext steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run: python main.py")
    else:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Add Quran data files to data/ directory")
        print("- Configure API keys in .env file")

if __name__ == "__main__":
    main() 