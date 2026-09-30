import os
import time
from dotenv import load_dotenv

from langchain_ollama import ChatOllama

# ============================================================
# LOAD ENVIRONMENT
# ============================================================
load_dotenv()

# ============================================================
# MODEL CONFIGURATION
# ============================================================
NODE_2_OLLAMA = ["llama3.2:3b"]
NODE_3_OLLAMA = ["llama3.2:3b"]

# ============================================================
# RESPONSE CONTENT EXTRACTION
# ============================================================
def extract_content(response):
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return content.get("text", str(content))
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(text)
        return "".join(parts)
    return str(content)

# ============================================================
# TOKEN USAGE EXTRACTION
# ============================================================
def extract_usage(response):
    usage = getattr(response, "usage_metadata", None)
    if isinstance(usage, dict):
        input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens") or 0
        output_tokens = usage.get("output_tokens") or usage.get("completion_tokens") or 0
        total_tokens = usage.get("total_tokens") or (input_tokens + output_tokens)
        return {
            "input_tokens": int(input_tokens),
            "output_tokens": int(output_tokens),
            "total_tokens": int(total_tokens)
        }

    response_metadata = getattr(response, "response_metadata", {})
    if isinstance(response_metadata, dict):
        token_usage = response_metadata.get("token_usage") or response_metadata.get("usage") or {}
        if isinstance(token_usage, dict):
            input_tokens = token_usage.get("input_tokens") or token_usage.get("prompt_tokens") or 0
            output_tokens = token_usage.get("output_tokens") or token_usage.get("completion_tokens") or 0
            total_tokens = token_usage.get("total_tokens") or (input_tokens + output_tokens)
            return {
                "input_tokens": int(input_tokens),
                "output_tokens": int(output_tokens),
                "total_tokens": int(total_tokens)
            }

    return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

# ============================================================
# LLM CLIENT
# ============================================================
class LLMClient:
    def __init__(self):
        pass  # no API keys needed — Ollama runs locally

    def _try_providers(self, prompt, ollama_models):
        for model_name in ollama_models:
            try:
                model = ChatOllama(model=model_name, temperature=0)
                start = time.time()
                response = model.invoke(prompt)
                latency = time.time() - start
                content = extract_content(response)
                usage = extract_usage(response)
                print(f"[LLM] Ollama {model_name} successful (local) | "
                      f"Tokens: {usage['input_tokens']}+{usage['output_tokens']}")
                return {
                    "content": content,
                    "provider": f"ollama/{model_name}",
                    "usage": usage,
                    "latency": latency
                }
            except Exception as e:
                print(f"[LLM] Ollama {model_name} failed: {e}")

        raise RuntimeError("Ollama provider failed. Is `ollama serve` running and the model pulled?")

    def invoke_generator(self, prompt):
        return self._try_providers(prompt, NODE_2_OLLAMA)

    def invoke_judge(self, prompt):
        return self._try_providers(prompt, NODE_3_OLLAMA)

# ============================================================
# GLOBAL CLIENT
# ============================================================
llm = LLMClient()