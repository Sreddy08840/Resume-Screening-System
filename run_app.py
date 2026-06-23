
"""Startup script for Resume Screening System"""
import os
import sys
import subprocess
import webbrowser
import time


def main():
    print("=" * 80)
    print("🚀 RESUME SCREENING SYSTEM - FULL STACK APPLICATION 🚀")
    print("=" * 80)
    
    # Install dependencies if needed
    print("\n📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start backend server
    print("\n🎯 Starting FastAPI backend server...")
    print("   Backend: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    # Open browser
    print("\n🌐 Opening application in browser...")
    time.sleep(2)
    file_path = os.path.abspath("index.html")
    webbrowser.open(f"file://{file_path}")
    
    print("\n✅ Application is now running!")
    print("   Please start the backend server in a separate terminal:")
    print("   python -m uvicorn api:app --reload")
    print("\n" + "=" * 80)
    
    # Start backend in current terminal
    os.system(f"{sys.executable} -m uvicorn api:app --reload")


if __name__ == "__main__":
    main()
