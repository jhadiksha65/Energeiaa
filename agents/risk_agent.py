from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=60.0)

def run_risk_agent(findings: str, parameters: str) -> list:
    print("⚠️ Risk Agent running...")

    prompt = f"""
You are a health risk analysis agent. Identify risk indicators from the medical findings.

Medical Findings: {findings}
Test Parameters: {parameters}

Return a JSON array of risk indicators. Each item must have exactly these keys:
- "name": short name of the risk (e.g. "High Blood Pressure")
- "level": exactly one of "Low", "Moderate", or "High"
- "explanation": 1-2 sentence plain English explanation of what this risk means

Include 3-5 risk indicators total.
Return ONLY valid JSON array. No extra text, no markdown, no code blocks.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )

    text = response.choices[0].message.content.strip()
    return json.loads(text)