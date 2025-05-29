import os
import sys
import requests
import json

def clean_text(text):
    return text.encode('ascii', errors='replace').decode('ascii')

diff_path = "code/temp/diff.txt"
with open(diff_path, "r", encoding="utf-8") as f:
    diff_content = f.read()

print(f"[DEBUG] Diff length before cleaning: {len(diff_content)}")

diff_content = clean_text(diff_content)

print(f"[DEBUG] Diff length after cleaning: {len(diff_content)}")

# Reduce max characters to limit input tokens
MAX_CHARS = 8000
if len(diff_content) > MAX_CHARS:
    diff_content = diff_content[-MAX_CHARS:]
    print(f"[DEBUG] Trimmed diff to last {MAX_CHARS} characters")

api_key = os.getenv("OPENAI_API_KEY", "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")

# Fix the OpenRouter API URL - it should end with /chat/completions
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/your-repo",  # OpenRouter requires this
    "X-Title": "Git Diff Summarizer"  # Optional but recommended
}

payload = {
    "model": "deepseek/deepseek-r1",  # Updated model name
    "max_tokens": 1000,
    "temperature": 0.7,
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes git diffs in clear, concise language."
        },
        {
            "role": "user",
            "content": (
                "Please summarize the following git diff changes:\n\n"
                f"{diff_content}\n\n"
                "Explain briefly what was changed (only in src/* directory). Keep the summary concise and under 200 words."
            )
        }
    ]
}

print(f"[DEBUG] Making request to: {url}")
print(f"[DEBUG] Using model: {payload['model']}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    print(f"[DEBUG] Response status code: {response.status_code}")
    print(f"[DEBUG] Response headers: {dict(response.headers)}")
    print(f"[DEBUG] Raw response text: {response.text[:500]}...")  # First 500 chars
    
    response.raise_for_status()
    
    # Check if response is empty
    if not response.text.strip():
        print("[ERROR] Empty response from API")
        sys.exit(1)
    
    try:
        resp_data = response.json()
    except json.JSONDecodeError as json_err:
        print(f"[ERROR] Failed to parse JSON response: {json_err}")
        print(f"[DEBUG] Raw response: {response.text}")
        sys.exit(1)
        
except requests.exceptions.HTTPError as http_err:
    print(f"[ERROR] HTTP error occurred: {http_err}")
    print(f"[DEBUG] Response text: {response.text}")
    sys.exit(1)
except requests.exceptions.RequestException as req_err:
    print(f"[ERROR] Request failed: {req_err}")
    sys.exit(1)

print(f"[DEBUG] Full response object:\n{json.dumps(resp_data, indent=2)}")

# Check for API errors in response
if 'error' in resp_data:
    print(f"[ERROR] API returned error: {resp_data['error']}")
    sys.exit(1)

try:
    explanation = resp_data['choices'][0]['message']['content'].strip()
except (KeyError, IndexError) as e:
    print(f"[ERROR] Unexpected response structure: {e}")
    print(f"[DEBUG] Available keys in response: {list(resp_data.keys())}")
    if 'choices' in resp_data and resp_data['choices']:
        print(f"[DEBUG] Available keys in first choice: {list(resp_data['choices'][0].keys())}")
    sys.exit(1)

if explanation == "":
    print("[WARN] The model returned an empty response.")
else:
    print("\n[RESPONSE]\n", explanation)

out_path = "code/temp/explanation.txt"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as out_f:
    out_f.write(explanation)
print(f"[INFO] Explanation written to {out_path}")