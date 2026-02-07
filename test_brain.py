import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.join(os.getcwd(), "Portfolio_Dev/field_notes"))

from ai_engine import AcmeLabClient

def test_brain_connection():
    logging.basicConfig(level=logging.INFO)
    client = AcmeLabClient()
    
    print("=== TESTING BRAIN CONNECTION ===")
    if client.prime():
        print("Success: Brain is awake.")
        response = client.generate("Ping? Answer 'Pong' if you receive this.")
        print(f"Brain Response: {response}")
    else:
        print("Error: Brain is unreachable. Check if Windows host 192.168.1.26 is online.")

if __name__ == "__main__":
    test_brain_connection()
