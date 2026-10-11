import os
import time
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_gemini(question, context):

    prompt = f"""
You are an AI assistant.

Answer ONLY using the information provided in the context.

If the answer is not available in the context, reply:
"I couldn't find the answer in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
"""

    # List of models to try (fallback if one is busy)
    models = [
        "gemini-3.5-flash",
        "gemini-flash-latest",
        "gemini-2.5-flash-lite"
    ]

    for model_name in models:
        try:
            print(f"🤖 Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            print(f"✅ Success using {model_name}")

            return response.text

        except Exception as e:
            print(f"❌ {model_name} failed: {e}")
            time.sleep(2)

    return "❌ All Gemini models are currently busy. Please try again in a few minutes."