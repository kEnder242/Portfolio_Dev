import os
import json
import glob
import sys
import hashlib
import re

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine_v2 import get_engine_v2

REASONING_MODE = "--reasoning" in sys.argv
HYBRID_MODE = "--hybrid" in sys.argv
engine_mode = "LOCAL"
if HYBRID_MODE: engine_mode = "HYBRID"
elif REASONING_MODE: engine_mode = "REASONING"

ENGINE = get_engine_v2(mode=engine_mode)
DATA_DIR = "field_notes/data"
RAW_DIR = "raw_notes"

# Context Files
FOCAL_OLD = "raw_notes/Performance review 2008-2018 .txt"
FOCAL_NEW = "raw_notes/11066402 Insights 2019-2024.txt"

# Hardcoded High-Value Synopses (Grounded Expertise)
STAR_SYNOP = {
    "riv_common.py": "Core PythonSV utility for managing device naming and named nodes in Simics.",
    "pecistressor.py": "High-throughput PECI command stress tool, capable of ~5300 commands/sec.",
    "blackbox.py": "System telemetry recorder for capturing post-mortem diagnostic data.",
    "redfish_utils.py": "Abstraction layer for scalable Redfish API interactions (GET/POST/PATCH).",
    "sensor_validator.py": "Automated validation of OpenBMC sensor thresholds against platform specs.",
    "mctp_wrapper.cpp": "C++ packet handling wrapper for low-latency MCTP communication.",
    "makechart.py": "Telemetry visualization tool converting raw PECI/RAPL logs into analytical charts.",
    "DTTC_2022_Peci_Stress.pdf": "Peer-reviewed paper on measuring and optimizing sideband telemetry performance.",
    "Philosophy and Learnings 2024.docx": "Comprehensive personal manifesto on validation logic and Class 1 design.",
    "Jason Allred - War stories (Work).docx": "The primary source text for engineering anecdotes and technical wins.",
    "MIV- Requirements for Automation.xlsx": "Comprehensive requirement matrix for manageability validation automation.",
    "MCTP Debug features.pptx": "Technical deep-dive into MCTP discovery and debugging architecture.",
    "MIV DTAF integration.pptx": "Architecture for integrating MIV with the Distributed Test Automation Framework.",
    "PECI_Comparison.xlsx": "Side-by-side technical comparison of PECI revisions and command support.",
    "pl1_pl2.txt": "Automated power limit (PL1/PL2) sweep and validation results.",
    "_Stressing Redfish PECI.pptx": "Presentation on the methodology for high-load Redfish-to-PECI stress testing.",
    "gethostcpudata.py": "Utility for extracting host CPU telemetry via sideband interfaces.",
    "peci_redfish.py": "Tool for bridging and validating PECI commands through Redfish endpoints.",
    "policy.py": "Platform power policy management and validation logic.",
    "Backup -MIV Blackbox Recorder.pptx": "Documentation on flight recorder analysis for platform failures.",
    "MIV for Execution.pptx": "Strategic execution plan for large-scale manageability validation.",
    "ras-viral.txt": "Technical notes and validation strategy for CPU Viral state handling."
}

# Curated List with Direct IDs and Boosted Ranks
CURATED_MAP = {
    "pecistressor.py": {"id": "1a95TKnx8eODfM5gdCSv6V07i0ZHL_3F1", "rank": 4},
    "blackbox.py": {"id": "1DVv5BQXU00Jyh22jZLQc6q8mVJCcKTxk", "rank": 4},
    "makechart.py": {"id": "1Rr684PJVPrXmIGe5fmmcR4fSUuyk4NHd", "rank": 4},
    "DTTC_2022_Peci_Stress.pdf": {"id": "1sgbcpgviOaqb0p64LfwEHOD7XQnGKM0m", "rank": 4},
    "sensor_validator.py": {"id": "17tWU4uGCSCcvyrU825KXm39uDfMg_FlX", "rank": 4},
    "mctp_wrapper.cpp": {"id": "1706VmAyfVN-DlZYT8jhagHUJOChFFl5N", "rank": 4},
    "redfish_utils.py": {"id": "1ZSD1HM8ymIDtORFwW5DcImWdUunYqJtw", "rank": 4},
    "Stressing Redfish PECI_demo.pptx": {"id": "1HUg9mETwcZF-KoFVw3hWlNcPlQ1tM7z5", "rank": 4},
    "Backup -MIV Blackbox Recorder.pptx": {"id": "1LgjAPhFAFk2YmuCwJVhdZWeRKTgIHU7d", "rank": 4},
    "MIV for Execution.pptx": {"id": "1byzuaJU1IwmJf2LZhVwCCWaigrCseGmW", "rank": 4},
    "gethostcpudata.py": {"id": "1IwlHtWG8jVpIACM55hM63C3vQf6xriYk", "rank": 4},
    "policy.py": {"id": "1bl8p8sKgvUG3fXVTi2XwHLdzxjprn-eD", "rank": 4},
    "pl1_pl2.txt": {"id": "1yq2UOrpkjA1G5u_SIxxgbq1HfTAVb8KK", "rank": 4},
    "MCTP Debug features.pptx": {"id": "1Zd14tG7tIabR1DOPXmPkrTg33Ds-vdW0", "rank": 4},
    "_Stressing Redfish PECI.pptx": {"id": "1-BeZ4N7l9ayq4XKZy-CslC3fOwN1V5Dm", "rank": 4},
    "peci_redfish.py": {"id": "1g482ua4P6Rj-g1NDMCGp3Sq3tuegQFEE", "rank": 4},
    "MIV DTAF integration.pptx": {"id": "1jQfX4aK3yvxzN_WxhPDKvv9QSQigAwc6", "rank": 4},
    "PECI_Comparison.xlsx": {"id": "1Kc9DsqzyIYOgTUZ5R7rgVW3rtD-xNl42", "rank": 4},
    "MIV Ignition-Redfish validation-Backup.pptx": {"id": "1sLjcbrxM3Bi9HMWmkuQPQRTvmSbVmrFJ", "rank": 3},
    "MIV- Requirements for Automation.xlsx": {"rank": 4},
    "riv_common.py": {"id": "1Vgs_Gr9wdk8nc3ByEn4jH859jK29Yut5", "rank": 4},
    "ras-viral.txt": {"id": "1Q6SyKK4_qb4VSp0YozQnQ03URVbum7lv", "rank": 4}
}

def is_binary(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    return ext in ['.xlsx', '.xls', '.pptx', '.ppt', '.pdf', '.doc', '.docx', '.zip', '.exe', '.dll', '.suo', '.ncb', '.idb', '.obj']

def read_file_sample(filepath, limit=4000):
    if is_binary(filepath):
        return f"[BINARY FILE] Filename: {os.path.basename(filepath)}"
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if len(content) > limit:
                mid = len(content) // 2
                return content[:limit//2] + "\n...[MID]...\n" + content[mid:mid+limit//2]
            return content[:limit]
    except Exception as e:
        return f"[ERROR READING FILE] {str(e)}"

def load_context():
    context = ""
    try:
        with open(FOCAL_NEW, 'r', encoding='utf-8', errors='ignore') as f:
            context += f"\n[FOCAL INSIGHTS 2019-2024]\n{f.read(4000)}"
    except: pass
    return context

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except: pass
    return None

def heuristic_rank(filename):
    if filename in CURATED_MAP:
        return CURATED_MAP[filename].get('rank', 3)
    f = filename.lower()
    if any(x in f for x in ['war stories', 'philosophy', 'dttc', 'architecture', 'retrospective', 'presentation']):
        return 4
    if f.endswith('.py') or f.endswith('.sh') or f.endswith('.cpp') or f.endswith('.c'):
        return 2
    if any(x in f for x in ['spec', 'datasheet', 'manual', 'guide']):
        return 1
    if any(x in f for x in ['log', 'dump', 'temp', 'backup', 'copy', 'raw', 'test']):
        return 0
    return 2

def heuristic_synopsis(filename):
    if filename in STAR_SYNOP:
        return STAR_SYNOP[filename]
    f = filename.lower()
    ext = os.path.splitext(f)[1]
    mapping = {
        ".py": "Python Script", ".sh": "Shell Script", ".cpp": "C++ Source",
        ".md": "Markdown Doc", ".pdf": "PDF Document", ".docx": "Word Doc",
        ".doc": "Word Doc", ".xlsx": "Spreadsheet", ".pptx": "Presentation Deck",
        ".txt": "Text Note"
    }
    return mapping.get(ext, "")

def scan_sector(year, curated_only=False):
    print(f"--- Artifact Scanner v2.0: {year} (Reasoning: {REASONING_MODE}) ---")
    if year.lower() in ["root", "docs"]:
        year_dir = RAW_DIR
        output_file = os.path.join(DATA_DIR, "artifacts_DOCS.json")
    else:
        year_dir = os.path.join(RAW_DIR, str(year))
        output_file = os.path.join(DATA_DIR, f"artifacts_{year}.json")
        if not os.path.exists(year_dir):
            return

    # Load existing
    artifacts = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            artifacts = json.load(f)
    
    existing_map = {item['filename']: item for item in artifacts}
    new_results = []

    # Get Files
    files_to_process = []
    IGNORE_TOKENS = ["resume", "review", "cover letter", "insights", "notes_", ".venv", ".git", "cheat sheet"]
    
    for root, dirs, files in os.walk(year_dir):
        if root != year_dir and not curated_only: continue 
        for name in files:
            if curated_only and name not in CURATED_MAP: continue
            if year.lower() in ["root", "docs"] and root == year_dir:
                if any(t in name.lower() for t in IGNORE_TOKENS): continue
            files_to_process.append(os.path.join(root, name))

    for filepath in sorted(files_to_process):
        filename = os.path.basename(filepath)
        print(f"Analyzing {filename}...")
        
        h_rank = heuristic_rank(filename)
        h_synopsis = heuristic_synopsis(filename)
        
        # Expert Override check
        is_star = filename in STAR_SYNOP
        
        data = None
        if not is_star:
            try:
                if REASONING_MODE and hasattr(ENGINE, 'generate_with_reasoning'):
                    # Use reasoning engine for artifacts
                    res_json_str = ENGINE.generate_with_reasoning(read_file_sample(filepath), bucket=year)
                    # Reasoning engine returns a list of events usually, but for artifacts we want one object
                    res_list = json.loads(res_json_str) if isinstance(res_json_str, str) else res_json_str
                    if res_list and len(res_list) > 0:
                        item = res_list[0]
                        data = {
                            "synopsis": item.get('summary', h_synopsis),
                            "rank": item.get('rank', h_rank),
                            "type": "Script" if filename.endswith('.py') else "Document",
                            "keywords": item.get('tags', [])
                        }
                else:
                    prompt = f"""
                    [TASK]
                    Analyze this file for a Senior Engineer's portfolio.
                    Return ONLY a JSON object. No conversational text.
                    
                    [FILENAME]
                    {filename}
                    [CONTENT SAMPLE]
                    {read_file_sample(filepath)}
                    
                    [REQUIREMENTS]
                    1. Synopsis: TERSE 1-sentence (max 12 words).
                    2. Rank: 0-4 (4=Showcase, 2=Standard, 0=Noise).
                    3. Keywords: 3-5 tags.
                    
                    [JSON FORMAT]
                    {{
                        "synopsis": "...",
                        "rank": 2,
                        "type": "Script" | "Document" | "Data",
                        "keywords": []
                    }}
                    """
                    response = ENGINE.generate(prompt)
                    data = extract_json(response)
            except Exception: pass
        
        if data and 'rank' in data:
            if filename in CURATED_MAP:
                data['rank'] = max(data['rank'], CURATED_MAP[filename].get('rank', 3))
            elif data['rank'] < h_rank:
                data['rank'] = h_rank
            data['filename'] = filename
            data['method'] = "AI (Reasoning)" if REASONING_MODE else "AI"
        else:
            data = {
                "filename": filename, "synopsis": h_synopsis,
                "rank": h_rank, "type": "Document" if h_rank > 2 else "Data", 
                "keywords": [], "method": "Heuristic"
            }
            if is_star: data['method'] = "Expert Hardcode"

        if filename in CURATED_MAP and 'id' in CURATED_MAP[filename]:
            data['drive_id'] = CURATED_MAP[filename]['id']
            
        new_results.append(data)
        print(f"   > [{data['method']}] Rank {data['rank']}")

    # Atomic Write Logic
    final_list = new_results
    seen = set(item['filename'] for item in new_results)
    if not curated_only:
        for item in artifacts:
            if item['filename'] not in seen:
                final_list.append(item)

    temp_file = output_file + ".tmp"
    with open(temp_file, 'w') as f:
        json.dump(final_list, f, indent=2)
    os.replace(temp_file, output_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Extract target (exclude --reasoning or --curated)
        targets = [a for a in sys.argv[1:] if not a.startswith('--')]
        if targets:
            target = targets[0]
            curated = "--curated" in sys.argv
            scan_sector(target, curated_only=curated)
        else:
            print("Usage: python3 scan_artifacts.py <year|docs|root> [--curated] [--reasoning]")

