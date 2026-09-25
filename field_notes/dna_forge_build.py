#!/usr/bin/env python3
"""
[FEAT-582 / FEAT-603] DNA Forge Build System Proxy
Delegates execution directly to modular build engine at Portfolio_Dev/dna_forge/dna_forge_build.py.
"""
import os
import sys
from pathlib import Path

DNA_FORGE_DIR = Path(__file__).resolve().parent.parent / "dna_forge"
sys.path.insert(0, str(DNA_FORGE_DIR))

try:
    from dna_forge_build import build_page
except ImportError:
    # Direct execution fallback
    import subprocess
    def build_page():
        subprocess.run([sys.executable, str(DNA_FORGE_DIR / "dna_forge_build.py")], check=True)

if __name__ == "__main__":
    build_page()
