import os
import json
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API key from .env
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=api_key)


def extract_query(user_query):
    """
    Extract the research topic and number of papers from the user's query.
    """

    prompt = f"""
You are an AI Research Assistant.

Your task is to extract:

1. Research Topic
2. Number of papers requested

Return ONLY valid JSON.

Example 1

User:
Give me 2 research papers on Machine Learning

Output:
{{
    "topic": "Machine Learning",
    "count": 2
}}

Example 2

User:
Find 10 papers on Generative AI

Output:
{{
    "topic": "Generative AI",
    "count": 10
}}

Example 3

User:
Show me research papers on AI in Healthcare

Output:
{{
    "topic": "AI in Healthcare",
    "count": 5
}}

If the user doesn't mention a number,
use 5 as the default count.

User:
{user_query}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        result = response.text.strip()

        # Remove markdown if Gemini returns ```json
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)

    except Exception as e:

        print("\nGemini Error:", e)

        # Fallback
        return {
            "topic": user_query,
            "count": 5
        }