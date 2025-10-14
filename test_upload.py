#!/usr/bin/env python
"""
Test script to verify the upload functionality works correctly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from parser import parse_resume

def test_parser():
    """Test the parser with the test resume"""
    print("Testing parser with test_resume.txt...")
    
    test_file = "test_resume.txt"
    if not os.path.exists(test_file):
        print(f"ERROR: {test_file} not found!")
        return False
    
    try:
        result = parse_resume(test_file, 'txt')
        print(f"✓ Parser successful!")
        print(f"  - Name: {result.get('name')}")
        print(f"  - Email: {result.get('email')}")
        print(f"  - Phone: {result.get('phone')}")
        print(f"  - Skills section: {result.get('skills_section', '')[:50]}...")
        print(f"  - Education: {result.get('education', '')[:50]}...")
        return True
    except Exception as e:
        print(f"✗ Parser failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RESUME SCREENER - PARSER TEST")
    print("=" * 60)
    
    success = test_parser()
    
    print("=" * 60)
    if success:
        print("✓ ALL TESTS PASSED!")
        print("\nYou can now:")
        print("1. Restart the backend: uv run backend/app.py")
        print("2. Upload resumes through the Streamlit UI")
    else:
        print("✗ TESTS FAILED - Please check the errors above")
    print("=" * 60)
