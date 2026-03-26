from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=60.0)

def run_coach_agent(findings: str, user_profile: dict, risk_indicators: list) -> dict:
    print("💡 Wellness Coach Agent running...")

    prompt = f"""
You are a personalized wellness coach agent. Based on the findings and risks, 
generate practical, motivating wellness advice.

User: {user_profile['name']}, {user_profile['age']} years old, {user_profile['occupation']}
Findings: {findings}
Risk Indicators: {json.dumps(risk_indicators)}

Return a JSON object with exactly these three keys:
- "wellness_insights": list of 3-4 positive insights about the person's health
- "recommendations": list of 4-5 specific, actionable recommendations
- "lifestyle_suggestions": list of 4-5 simple daily lifestyle changes with an emoji at the start of each

Return ONLY valid JSON. No extra text, no markdown, no code blocks.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )

    text = response.choices[0].message.content.strip()
    return json.loads(text)