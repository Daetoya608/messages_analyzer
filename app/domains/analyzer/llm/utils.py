import re

from langchain_ollama import ChatOllama


def get_ollama_llm(model="qwen3:8b-q4_K_M", base_url="http://localhost:11434"):
    return ChatOllama(
        model=model,
        temperature=0,
        base_url=base_url,
    )

def strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL|re.IGNORECASE)
