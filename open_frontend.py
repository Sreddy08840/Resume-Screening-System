
"""Simple script to open the frontend in your default browser"""
import os
import webbrowser
import sys


def main():
    print("=" * 60)
    print("🚀 RESUME SCREENING SYSTEM - OPENING FRONTEND 🚀")
    print("=" * 60)
    
    # Get absolute path to index.html
    html_path = os.path.abspath("index.html")
    
    if os.path.exists(html_path):
        print(f"\n🌐 Opening frontend in default browser...")
        print(f"📄 File: {html_path}")
        webbrowser.open(f"file://{html_path}")
        
        print("\n✅ Frontend is now open!")
        print("\n📝 Important:")
        print("   Please make sure the backend server is running!")
        print("   Start backend with: py -m uvicorn api:app --reload")
        print("\n" + "=" * 60)
    else:
        print(f"\n❌ Error: index.html not found at {html_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
