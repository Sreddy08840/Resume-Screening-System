
import os
from parser.resume_parser import ResumeParser

pdf_path = os.path.join(os.getcwd(), 'data', 'resumes', 'Santosh_Resume(full).pdf')
print("Testing PDF parse:", pdf_path)
result = ResumeParser.parse_single(pdf_path)
print("\nSuccess:", result['success'])

if result['success']:
    print("\n✅ Success! Extracted text")
    print(f"Text length: {len(result['raw_text'])} characters")
    print("\nFirst part:\n", result['raw_text'][:1000])
else:
    print("\n❌ Failed:", result['error'])
