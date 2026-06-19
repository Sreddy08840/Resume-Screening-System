
import os
from config import Config
from parser import ResumeParser


def main():
    print("=" * 60)
    print("Resume Parser Example")
    print("=" * 60)
    
    # Example 1: Parse multiple resumes from a directory
    print("\n1. Parsing resumes from data/resumes/ directory...")
    results = ResumeParser.parse_multiple(Config.RESUMES_DIR)
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\nTotal files processed: {len(results)}")
    print(f"Successfully parsed: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    
    for result in results:
        print(f"\n--- {result['file_name']} ---")
        if result['success']:
            print(f"Raw text length: {len(result['raw_text'])} characters")
            if 'cleaned_text' in result:
                print(f"Cleaned text length: {len(result['cleaned_text'])} characters")
        else:
            print(f"Error: {result['error']}")
    
    # Example 2: Parse a single resume
    if Config.RESUMES_DIR and os.path.exists(Config.RESUMES_DIR):
        files = [f for f in os.listdir(Config.RESUMES_DIR) 
                 if os.path.isfile(os.path.join(Config.RESUMES_DIR, f))]
        if files:
            sample_file = os.path.join(Config.RESUMES_DIR, files[0])
            print(f"\n2. Parsing single file: {files[0]}")
            try:
                single_result = ResumeParser.parse_single(sample_file)
                print("Success!")
                print(f"File name: {single_result['file_name']}")
                preview = single_result['raw_text'][:200].replace('\n', ' ')
                print(f"Raw text preview (first 200 chars): {preview}...")
            except Exception as e:
                print(f"Failed: {e}")


if __name__ == "__main__":
    main()

