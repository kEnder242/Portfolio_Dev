import requests
import json
import logging

# --- CONFIGURATION ---
DEFAULT_MODEL = "mistral:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

class CognitiveEngine:
    """
    Abstract Base Class for the AI Interface.
    Use this to decouple the Portfolio logic from the specific AI provider.
    """
    def generate(self, prompt, context="", options=None):
        raise NotImplementedError("Subclasses must implement generate()")

class OllamaClient(CognitiveEngine):
    """
    Direct Model Access (DMA) client.
    Connects directly to the local Ollama instance (Port 11434).
    Fast, stateless, robust.
    """
    def __init__(self, model=DEFAULT_MODEL, url=OLLAMA_URL):
        self.model = model
        self.url = url

    def generate(self, prompt, context="", options=None):
        """
        Generates a response from Ollama.
        """
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": options or {"temperature": 0.1, "num_ctx": 8192}
        }
        
        try:
            # 60s timeout to prevent hangs
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            logging.error(f"Ollama Error: {e}")
            return "{}"

class AcmeLabClient(CognitiveEngine):
    """
    [STUB] Future Client for HomeLabAI Integration.
    Will connect via MCP or WebSocket to 'Pinky' (The Agent).
    """
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
    
    def generate(self, prompt, context="", options=None):
        # TODO: Implement MCP Client Logic here.
        # client = mcp.Client(self.host, self.port)
        # return client.call_tool("archive_notes", {"text": prompt})
        print("AcmeLabClient is not yet implemented. Please use OllamaClient.")
        return "{}"

# --- FACTORY ---
def get_engine(mode="LOCAL"):
    if mode == "LOCAL":
        return OllamaClient()
    elif mode == "LAB":
        return AcmeLabClient()
    else:
        raise ValueError(f"Unknown engine mode: {mode}")
