from openai import OpenAI

# Use Ollama's OpenAI-compatible endpoint
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # any string works, just required by the SDK
)

def ask_ollama(system_prompt: str, user_prompt: str):
    response = client.chat.completions.create(
        model="llama3.1:8b",   # match the Ollama model tag
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=200
    )
    return response.choices[0].message.content