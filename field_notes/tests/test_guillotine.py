import sys
import os
import re
import logging

# Set up logging for test
logging.basicConfig(level=logging.INFO)

# Add the directory to sys.path to import nibble_v2
sys.path.append(os.path.abspath("Portfolio_Dev/field_notes"))
from nibble_v2 import scrub_input_buffer

def test_guillotine():
    text = """
Header: 2024 Technical Goals
- Goal 1: Build a better lab.
- Goal 2: Implement faster inference.

AREAS FOR IMPROVEMENT
Jason should work more on documentation.
Needs to improve on parallel processing.

Next Year's Technical Strategy
- Implement multi-agent consensus.
- Add more telemetry.
"""
    print("Testing Structural Guillotine...")
    result = scrub_input_buffer(text)
    print("--- RESULT ---")
    print(result)
    print("--- END ---")
    
    # Check if forbidden section is removed
    forbidden_found = "AREAS FOR IMPROVEMENT" in result or "Jason should" in result
    # Check if safe section is present
    safe_found = "Next Year's Technical Strategy" in result
    
    if not forbidden_found and safe_found:
        print("\nOVERALL: PASS")
    else:
        print("\nOVERALL: FAIL")
        if forbidden_found: print("  - Reason: Forbidden section found.")
        if not safe_found: print("  - Reason: Safe section missing.")

if __name__ == "__main__":
    test_guillotine()
