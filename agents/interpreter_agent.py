from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=60.0)

def run_interpreter_agent(findings: str, parameters: str, observations: str) -> dict:
    print("🔬 Interpreter Agent running...")

    prompt = f"""
You are a medical interpreter agent. Convert technical medical findings into simple, 
friendly language that a non-medical person can easily understand.

Medical Findings: {findings}
Test Parameters: {parameters}
Observations: {observations}

Return a JSON object with exactly these two keys:
- "key_observations": a list of 4-5 short plain-English bullet points summarizing what was found
- "interpretations": a list of 4-5 plain-English explanations of what each finding means for the person

Return ONLY valid JSON. No extra text, no markdown, no code blocks.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )

    text = response.choices[0].message.content.strip()
    return json.loads(text)