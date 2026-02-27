import requests
import json
import logging
import os
import glob
import re
from ai_engine import OllamaClient, get_engine, CognitiveEngine

# Try to import Liger/Transformers for DMA mode
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from liger_kernel.transformers import apply_liger_kernel_to_llama
    HAS_LIGER = True
except ImportError:
    HAS_LIGER = False

# --- CONFIGURATION ---
DEFAULT_MODEL = "llama3.2:1b"
DMA_MODEL_PATH = "casperhansen/llama-3.2-3b-instruct-awq"
OLLAMA_URL = "http://localhost:11434/api/generate"
VLLM_URL = "http://localhost:8088/v1/completions"
DATA_DIR = "field_notes/data"
RAW_DIR = "raw_notes"

class VLLMClient(OllamaClient):
    """
    OpenAI-compatible client for vLLM server.
    """
    def __init__(self, url=VLLM_URL, model="llama-3.2-3b-awq"):
        super().__init__()
        self.url = url
        self.model = model

    def generate(self, prompt, context="", options=None):
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "max_tokens": options.get("num_predict", 512) if options else 512,
            "temperature": options.get("temperature", 0.1) if options else 0.1,
            "stream": False
        }
        try:
            resp = requests.post(self.url, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                return data['choices'][0]['text']
            else:
                logging.error(f"vLLM Error ({resp.status_code}): {resp.text}")
                return ""
        except Exception as e:
            logging.error(f"vLLM Connection Failed: {e}. Falling back to Ollama.")
            return super().generate(prompt, context, options)

class LigerEngine(OllamaClient):
    """
    Direct Model Access (DMA) with Liger-Kernel optimization.
    Provides ~80% VRAM reduction on Turing GPUs.
    """
    def __init__(self, model_path=DMA_MODEL_PATH):
        super().__init__()
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self._initialized = False

    def _initialize(self):
        if self._initialized: return
        logging.info(f"Initializing LigerEngine with {self.model_path}...")
        try:
            # Llama 2, 3, 3.1, and 3.2 share the same base architecture in Liger
            apply_liger_kernel_to_llama()
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            self._initialized = True
            logging.info("LigerEngine initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize LigerEngine: {e}. Falling back to Ollama.")
            self._initialized = False

    def generate(self, prompt, context="", options=None):
        if not self._initialized:
            self._initialize()
        
        if not self._initialized:
            return super().generate(prompt, context, options)

        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=options.get("num_predict", 512) if options else 512,
                temperature=options.get("temperature", 0.1) if options else 0.1
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- DOCUMENT TIERS (The 'QQ' Mapping) ---
DOCUMENT_TIERS = {
    "PHILOSOPHY": ["Philosophy and Learnings 2024.docx", "WWW_STRATEGY.md", "DEV_LAB_STRATEGY.md"],
    "RESUME": ["Jason Allred Resume - Jan 2026.txt", "Jason Allred Resume - Dec 2025.txt"],
    "FOCAL": ["11066402 Insights 2019-2024.txt", "Performance review 2008-2018 .txt"],
    "NOTE": ["notes_*.txt", "ras-*.txt"],
    "ARTIFACT": ["*.py", "*.sh", "*.cpp", "*.pdf", "*.pptx", "*.xlsx"]
}

class ArchiveMemory:
    """
    FS-Researcher / RLM Implementation.
    Treats the file system as durable external memory.
    """
    def __init__(self, data_dir=DATA_DIR, raw_dir=RAW_DIR):
        self.data_dir = data_dir
        self.raw_dir = raw_dir
        self._tool_registry = self._build_tool_registry()

    def _build_tool_registry(self):
        """
        Maps specific scripts/artifacts to their directory-based 'Era'.
        Example: riv_common.py -> 2019
        """
        registry = {}
        # Scan year directories in raw_notes
        for year in range(2000, 2027):
            path = os.path.join(self.raw_dir, str(year))
            if os.path.exists(path):
                files = os.listdir(path)
                for f in files:
                    registry[f] = str(year)
        return registry

    def get_context(self, bucket=None, raw_text=""):
        """
        Retrieves historical context for a specific bucket (e.g., '2024-01').
        Implements Agentic-R utility-based re-ranking.
        """
        context = ""
        
        # 1. Inject Tool Registry Era-Awareness
        context += "\n[TOOL ERA REGISTRY]\n"
        # Only inject tools relevant to the potential context (sample some or all if small)
        for tool, year in self._tool_registry.items():
            if tool.endswith('.py') or tool.endswith('.sh'):
                context += f"- {tool}: Released {year}\n"

        # 2. Agentic-R: Utility-Based Re-Ranking
        if raw_text:
            context += "\n[RELEVANT HISTORICAL WINS (Utility Ranked)]\n"
            # Extract potential keywords (simple word extraction)
            keywords = re.findall(r'\b\w{4,}\b', raw_text.lower())
            potential_events = []
            
            # Scan all JSON files in data dir
            json_files = glob.glob(os.path.join(self.data_dir, "*.json"))
            for jf in json_files:
                if "themes" in jf or "status" in jf or "search_index" in jf: continue
                try:
                    with open(jf, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            for event in data:
                                # Rank based on keyword hits in summary/evidence/tags
                                text_to_check = (event.get('summary', '') + " " + 
                                               event.get('evidence', '') + " " + 
                                               " ".join(event.get('tags', []))).lower()
                                hits = sum(1 for kw in keywords if kw in text_to_check)
                                if hits > 0:
                                    potential_events.append((hits, event))
                except: pass
            
            # Sort by hits DESC and take top 3
            potential_events.sort(key=lambda x: x[0], reverse=True)
            seen_summaries = set()
            count = 0
            for _, event in potential_events:
                if event.get('summary') not in seen_summaries:
                    context += f"- {event.get('date')}: {event.get('summary')} (Ref: {event.get('evidence')[:100]}...)\n"
                    seen_summaries.add(event.get('summary'))
                    count += 1
                if count >= 3: break

        # 3. Chronological Continuity (Previous month)
        if bucket and '-' in bucket:
            try:
                y, m = map(int, bucket.split('-'))
                prev_m = m - 1 if m > 1 else 12
                prev_y = y if m > 1 else y - 1
                prev_bucket = f"{prev_y}-{str(prev_m).zfill(2)}"
                prev_file = os.path.join(self.data_dir, f"{prev_bucket.replace('-', '_')}.json")
                if os.path.exists(prev_file):
                    with open(prev_file, 'r') as f:
                        data = json.load(f)
                        if data:
                            # Just take the last 2 entries for context
                            context += f"\n[CHRONOLOGICAL CONTEXT ({prev_bucket})]\n"
                            context += json.dumps(data[-2:], indent=2)
            except: pass

        # 4. Get Themes
        theme_file = os.path.join(self.data_dir, "themes.json")
        if os.path.exists(theme_file):
            with open(theme_file, 'r') as f:
                themes = json.load(f)
                year = bucket.split('-')[0] if bucket else None
                if year and year in themes:
                    context += f"\n[STRATEGIC THEME ({year})]\n{themes[year].get('strategic_theme', '')}"
        
        return context

class SemanticCondenser:
    """
    Apple CLaRa Implementation.
    Compresses raw text into high-density technical abstracts (16x-128x).
    """
    def __init__(self, client):
        self.client = client

    def condense(self, text):
        prompt = f"""
        [TASK]
        Compress the following technical log into a high-density 'Technical Abstract'.
        Preserve ALL specific tool names, error codes, and architectural decisions.
        Remove all conversational filler and redundant dates.
        
        [RAW LOG]
        {text[:8000]}
        
        [OUTPUT FORMAT]
        One paragraph of high-density technical prose.
        """
        return self.client.generate(prompt)

class CurriculumEngine(CognitiveEngine):
    """
    TTCS (Test-Time Curriculum Synthesis) Implementation.
    Uses a Synthesize-then-Solve loop to improve reasoning quality.
    """
    def __init__(self, backend=None):
        # Prefer DMA/Liger for local reasoning to save VRAM
        if not backend:
            if HAS_LIGER:
                self.local_backend = LigerEngine()
            else:
                self.local_backend = OllamaClient()
        else:
            self.local_backend = backend
            
        self.backend = self.local_backend
        self.memory = ArchiveMemory()
        self.condenser = SemanticCondenser(self.backend)

    def generate(self, prompt, context="", options=None):
        return self.backend.generate(prompt, context, options)

    def generate_with_reasoning(self, raw_text, bucket=None):
        logging.info(f"Starting Curriculum Reasoning for {bucket}...")
        
        # 1. FS-Researcher & Agentic-R: Inject History + Utility Ranking
        history = self.memory.get_context(bucket, raw_text)
        
        # 2. CLaRa: Semantic Compression
        abstract = self.condenser.condense(raw_text)
        
        # 3. TTCS Phase 1: Synthesize Anchors
        synth_prompt = f"""
        [GROUNDING: ERA AWARENESS]
        {history}
        
        [GROUNDING: DOCUMENT TIERS]
        - FOCAL: Strategic high-level goals.
        - NOTE: Daily tactical logs.
        - ARTIFACT: Released tools (see Era Registry for dates).
        
        [TECHNICAL ABSTRACT]
        {abstract}
        
        [TASK]
        Synthesize 3 'Technical Anchors' (challenging questions) that this text answers.
        
        [STRICTNESS RULES]
        1. If the [TECHNICAL ABSTRACT] is sparse, generic, or only contains links/TODOs, do NOT synthesize technical questions about servers, backups, or installations.
        2. Instead, synthesize one anchor: "What is the primary TODO or research link mentioned?"
        3. Do not invent technical issues (e.g. SSD errors, permissions) that are not in the text.
        4. Ensure tool associations match the [TOOL ERA REGISTRY].
        """
        anchors = self.backend.generate(synth_prompt)
        
        # 4. TTCS Phase 2: Solve
        solve_prompt = f"""
        [RAW LOGS]
        {raw_text[:6000]}
        [TECHNICAL ANCHORS]
        {anchors}
        
        [TASK]
        Solve the anchors using evidence from the RAW LOGS.
        **CRITICAL:** Verify the year of the log against the tool's release year.
        If there is a conflict (e.g., tool released in 2022 used in a 2019 note), flag it as a [CAUSALITY ERROR] and ignore the tool name.
        """
        solutions = self.backend.generate(solve_prompt)
        
        # 5. Final Consolidation
        final_prompt = f"""
        [ROLE] Expert Technical Archivist.
        [BKM PROTOCOL] 1. One-liner, 2. Core Logic, 3. Trigger, 4. Scars.
        
        [SOLUTIONS]
        {solutions}
        [HISTORY]
        {history}
        
        [STRICT EVIDENCE RULE]
        1. ONLY extract events explicitly mentioned in the [SOLUTIONS] or [RAW LOGS].
        2. If the text is just a date, a TODO, or a link, return an empty list [].
        3. NEVER invent web server installs (Apache/Nginx) or database setups unless the text says so.
        4. If a tool from [HISTORY] is not in the [RAW LOGS], do not mention it.
        
        [TASK]
        Generate a JSON list of technical events for the archive.
        Redact personal names/emails with [REDACTED].
        
        [REF] docs/plans/RESEARCH_SYNTHESIS.md
        
        [JSON FORMAT]
        [
          {{ "date": "YYYY-MM-DD", "summary": "...", "evidence": "...", "sensitivity": "Public", "tags": [] }}
        ]
        """
        return self.backend.generate(final_prompt)

def get_engine_v2(mode="LOCAL"):
    if mode == "VLLM":
        return VLLMClient()
    elif mode == "REASONING":
        return CurriculumEngine()
    elif mode == "DMA":
        return LigerEngine()
    elif mode == "LAB":
        from ai_engine import AcmeLabClient
        client = AcmeLabClient()
        client.prime()
        return client
    elif mode == "HYBRID":
        from ai_engine import AcmeLabClient
        brain = AcmeLabClient()
        brain.prime()
        return CurriculumEngine(backend=brain)
    return get_engine(mode)
