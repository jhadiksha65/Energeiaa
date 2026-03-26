from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=60.0)
def run_profile_agent(user_profile: dict, findings: str) -> str:
    print("🤖 Profile Agent running...")

    prompt = f"""
You are a medical profile summarization agent.
Given this user profile and their medical findings, write a warm, friendly 2-3 sentence 
profile summary for a wellness report. Use simple language. No medical jargon.

User Profile:
- Name: {user_profile['name']}
- Age: {user_profile['age']}
- Gender: {user_profile['gender']}
- Occupation: {user_profile.get('occupation', 'Not provided')}
- Medical History: {user_profile.get('medical_history', 'None')}

Doctor's Findings: {findings}

Return ONLY the profile summary text. No extra formatting.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content.strip()