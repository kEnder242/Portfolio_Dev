import os
import glob

DATA_DIR = "field_notes/data"

def clean():
    print("--- Cleaning Artifact Data ---")
    files = glob.glob(os.path.join(DATA_DIR, "artifacts_*.json"))
    if not files:
        print("No artifact files found.")
        return

    for f in files:
        try:
            os.remove(f)
            print(f"Removed: {f}")
        except Exception as e:
            print(f"Error removing {f}: {e}")

    print("Cleanup complete.")

if __name__ == "__main__":
    clean()
