import time
from agents.profile_agent import run_profile_agent
from agents.interpreter_agent import run_interpreter_agent
from agents.risk_agent import run_risk_agent
from agents.coach_agent import run_coach_agent
from agents.compiler_agent import run_compiler_agent

def call_with_retry(func, *args, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return func(*args)
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                print(f"🔄 Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise

def calculate_wellness_score(risk_indicators: list) -> int:
    score = 100
    for risk in risk_indicators:
        level = risk.get("level", "Low")
        if level == "High":
            score -= 20
        elif level == "Moderate":
            score -= 10
        elif level == "Low":
            score -= 5
    return max(0, min(100, score))

def run_pipeline(user_profile: dict, findings: str, parameters: str, observations: str) -> dict:
    print("\n🚀 Starting Energeiaa Agent Pipeline...\n")

    profile_summary = call_with_retry(run_profile_agent, user_profile, findings)
    interpreter_output = call_with_retry(run_interpreter_agent, findings, parameters, observations)
    risk_indicators = call_with_retry(run_risk_agent, findings, parameters)
    coach_output = call_with_retry(run_coach_agent, findings, user_profile, risk_indicators)
    wellness_score = calculate_wellness_score(risk_indicators)

    final_report = run_compiler_agent(
        profile_summary,
        interpreter_output,
        risk_indicators,
        coach_output,
        wellness_score
    )

    print("\n✅ Pipeline complete!")
    return final_report