import os
import sys
from openai import OpenAI

def clean_text(text):
    return text.encode('ascii', errors='replace').decode('ascii')

diff_path = "code/temp/diff.txt"
with open(diff_path, "r", encoding="utf-8") as f:
    diff_content = f.read()

print(f"[DEBUG] Diff length before cleaning: {len(diff_content)}")

diff_content = clean_text(diff_content)

print(f"[DEBUG] Diff length after cleaning: {len(diff_content)}")

# Reduce max characters to limit input tokens
MAX_CHARS = 8000  # Reduced from 60000 to limit token usage
if len(diff_content) > MAX_CHARS:
    diff_content = diff_content[-MAX_CHARS:]
    print(f"[DEBUG] Trimmed diff to last {MAX_CHARS} characters")

api_key = os.getenv("OPENAI_API_KEY", "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")
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

try:
    resp = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528",
        max_tokens=1000,  # Limit output tokens to stay within budget
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes git diffs in clear, concise language."
            },
            {
                "role": "user",
                "content": (
                    "Please summarize the following git diff changes:\n\n"
                    f"{diff_content}\n\n"
                    "Explain briefly what was changed. Keep the summary concise and under 200 words."
                )
            }
        ],
    )
except Exception as e:
    print(f"[ERROR] API call failed: {e}")
    sys.exit(1)

print(f"[DEBUG] Full response object:\n{resp}")

explanation = resp.choices[0].message.content.strip()

if explanation == "":
    print("[WARN] The model returned an empty response.")
else:
    print("\n[RESPONSE]\n", explanation)

out_path = "code/temp/explanation.txt"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as out_f:
    out_f.write(explanation)
print(f"[INFO] Explanation written to {out_path}")