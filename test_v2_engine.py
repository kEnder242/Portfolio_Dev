import sys
import os

# Add current directory to path
sys.path.append(os.path.join(os.getcwd(), "Portfolio_Dev/field_notes"))

from ai_engine_v2 import CurriculumEngine

def test_reasoning_loop():
    engine = CurriculumEngine()
    
    # Explicit Mismatch:
    sample_text = """
    10/12/2024 - Updated riv_common.py to fix a 2024 Simics issue. 
    """
    
    print("=== STARTING TTCS BENCH-TEST (Explicit Era Mismatch) ===")
    response = engine.generate_with_reasoning(sample_text, bucket="2024-10")
    print("\n=== FINAL OUTPUT ===")
    print(response)

if __name__ == "__main__":
    test_reasoning_loop()
