from openai import OpenAI
import sys

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="deepseek/deepseek-r1-0528",
    messages=[
        {"role": "user", "content": sys.argv[1]}
    ]
)

print(response.choices[0].message.content)

