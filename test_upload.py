
import os
from parser.resume_parser import ResumeParser
from parser.pdf_parser import PDFParser

pdf_path = os.path.join(os.path.dirname(__file__), 'data', 'resumes', 'Santosh_Resume(full).pdf')
print("Testing PDF parse:", pdf_path)
print("File exists:", os.path.exists(pdf_path))
print("File size:", os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0, "bytes")

try:
    text = PDFParser.parse(pdf_path)
    print("\n✅ Success! Extracted text length:", len(text))
    print("First 500 characters:\n", text[:500])
except Exception as e:
    print("\n❌ Error parsing PDF:", e)
    import traceback
    traceback.print_exc()
