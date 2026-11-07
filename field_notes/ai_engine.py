import logging

import requests

# --- CONFIGURATION ---
DEFAULT_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"


class CognitiveEngine:
    """
    Abstract Base Class for the AI Interface.
    Use this to decouple the Portfolio logic from the specific AI provider.
    """

    def generate(self, prompt, context="", options=None):
        raise NotImplementedError("Subclasses must implement generate()")


class LocalEngineClient(CognitiveEngine):
    """
    Direct Local Engine client (llama-server on Port 8088).
    Connects directly to the sovereign dual-GPU MoE engine (35+ tok/s).
    """

    def __init__(
        self,
        url="http://127.0.0.1:8088/v1/chat/completions",
        model="local",
    ):
        self.url = url
        self.model = model

    def generate(self, prompt, context="", options=None):
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": (options or {}).get("temperature", 0.1),
            "max_tokens": 2048,
        }
        try:
            resp = requests.post(self.url, json=payload, timeout=90)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"LocalEngineClient error: {e}")
            return None


# Backward-compatible alias
UnifiedBaseClient = LocalEngineClient


class OllamaClient(CognitiveEngine):
    """
    Direct Model Access (DMA) client.
    Connects directly to the local Ollama instance (Port 11434).
    Fast, stateless, robust.
    """

    def __init__(self, model=DEFAULT_MODEL, url=OLLAMA_URL):
        self.url = url
        self.model = model  # Default

        try:
            tags_url = url.replace("/api/generate", "/api/tags")
            response = requests.get(tags_url, timeout=5)
            response.raise_for_status()
            models = [m.get("name") for m in response.json().get("models", [])]

            if not models:
                logging.warning(
                    "Ollama /api/tags returned no models. Using configured default."
                )
                return

            if model in models:
                self.model = model
            else:
                logging.warning(f"Model '{model}' not found in Ollama.")
                # Find a non-embedding model as a fallback
                fallback_model = next((m for m in models if "embed" not in m), None)

                if fallback_model:
                    self.model = fallback_model
                    logging.warning(
                        f"Falling back to first available model: {self.model}"
                    )
                else:
                    logging.error("No suitable fallback models found in Ollama.")
                    # Stick with original model and likely fail
        except Exception as e:
            logging.error(
                f"Failed to probe Ollama for models: {e}. Using configured default."
            )

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
            "options": options or {"temperature": 0.1, "num_ctx": 8192},
        }

        try:
            # 120s timeout for reasoning-heavy tasks on 11GB VRAM
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logging.error(f"Ollama Error: {e}")
            return None


class AcmeLabClient(CognitiveEngine):
    """
    Direct Bridge to 'The Brain' (Windows / 4090).
    Used for high-value synthesis and BKM-style report writing.
    """

    def __init__(
        self, url="http://192.168.1.26:11434/api/generate", model="llama3:latest"
    ):
        self.url = url
        self.model = model

    def prime(self):
        """Wakes up the Windows GPU model."""
        logging.info(f"Priming The Brain ({self.model})...")
        try:
            # Bypass proxies for local network
            proxies = {"http": None, "https": None}
            payload = {
                "model": self.model,
                "prompt": "wake up",
                "keep_alive": "10m",
                "stream": False,
            }
            # 90s timeout for cold-start model loading on Windows
            requests.post(self.url, json=payload, timeout=90, proxies=proxies)
            return True
        except Exception as e:
            logging.error(f"Prime failed: {e}")
            return False

    def generate(self, prompt, context="", options=None):
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": options or {"temperature": 0.1, "num_ctx": 8192},
        }
        try:
            proxies = {"http": None, "https": None}
            # 120s timeout for complex brain reasoning
            response = requests.post(
                self.url, json=payload, timeout=120, proxies=proxies
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logging.error(f"Brain Connection Failed: {e}. Falling back to Pinky.")
            # Fallback to local Ollama
            return OllamaClient().generate(prompt, context, options)


# --- FACTORY ---
def get_engine(mode="LOCAL"):
    if mode == "LOCAL":
        # Check if unified-base on port 8088 is available
        try:
            r = requests.get("http://127.0.0.1:8088/health", timeout=1)
            if r.status_code == 200:
                return UnifiedBaseClient()
        except Exception:
            pass
        return OllamaClient()
    elif mode == "LAB":
        return AcmeLabClient()
    elif mode == "UNIFIED":
        return UnifiedBaseClient()
    else:
        raise ValueError(f"Unknown engine mode: {mode}")
