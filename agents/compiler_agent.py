def run_compiler_agent(
    profile_summary: str,
    interpreter_output: dict,
    risk_indicators: list,
    coach_output: dict,
    wellness_score: int
) -> dict:
    print("📋 Compiler Agent running...")

    return {
        "profile_summary": profile_summary,
        "key_observations": interpreter_output.get("key_observations", []),
        "interpretations": interpreter_output.get("interpretations", []),
        "risk_indicators": risk_indicators,
        "wellness_insights": coach_output.get("wellness_insights", []),
        "recommendations": coach_output.get("recommendations", []),
        "lifestyle_suggestions": coach_output.get("lifestyle_suggestions", []),
        "wellness_score": wellness_score
    }