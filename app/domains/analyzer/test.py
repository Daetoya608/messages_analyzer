from langchain_core.messages.tool import tool_call
from langchain_ollama import ChatOllama

def get_ollama_llm(model="qwen3:8b-q4_K_M", base_url="http://localhost:11434"):
    return ChatOllama(
        model=model,
        temperature=0,
        base_url=base_url,
    )

if __name__ == "__main__":
    llm = get_ollama_llm()
    response = llm.invoke("Кто ты?")
    print(response.content)
