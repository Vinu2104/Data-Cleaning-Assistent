
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def ai_suggestions(df):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "API key not found. Add OPENAI_API_KEY "
            "to your .env file."
        )

    try:
        client = OpenAI(api_key=api_key)

        sample = df.head(10).to_string()

        prompt = f"""
You are a data cleaning expert.

Analyze this dataset sample:
{sample}

Suggest ways to improve:
1. Missing values
2. Duplicate rows
3. Possible outliers
4. Incorrect data types
5. Inconsistent text formats

Give simple, practical suggestions.
Do not claim to have changed the dataset.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI analysis failed: {e}"
