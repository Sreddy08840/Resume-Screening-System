
"""Simple script to open the frontend in your default browser"""
import os
import webbrowser


def main():
    html_path = os.path.abspath("index.html")
    
    if os.path.exists(html_path):
        print("Opening frontend in browser...")
        webbrowser.open(f"file://{html_path}")
        print("Done!")
        print("\nMake sure backend server is running!")
        print("Start backend with: py -m uvicorn api:app --reload")
    else:
        print("index.html not found!")


if __name__ == "__main__":
    main()
