import os, time, requests
from src.prompt_design import PROMPT_SYSTEM, PROMPT_USER_TEMPLATE

API_HOST = os.getenv("LMSTUDIO_HOST", "http://127.0.0.1:1234")
API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
MODEL = os.getenv("LM_MODEL", "gpt-oss-7b-instruct")
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

def query_model(story: str, timeout: int = 60):
    url = f"{API_HOST}/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM},
            {"role": "user", "content": PROMPT_USER_TEMPLATE.format(story=story)}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }
    t0 = time.time()
    r = requests.post(url, json=payload, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    resp = r.json()
    text = resp["choices"][0]["message"]["content"]
    rt = time.time() - t0
    return text, rt

