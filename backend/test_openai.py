from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

print("Key loaded:", key[:12] if key else "NO KEY")

client = OpenAI(
    api_key=key
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Say hello in one sentence"
        }
    ]
)

print(response.choices[0].message.content)