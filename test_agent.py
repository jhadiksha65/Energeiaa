from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import run_pipeline

user_profile = {
    "name": "Priya Sharma",
    "age": 35,
    "gender": "Female",
    "occupation": "Software Engineer",
    "medical_history": "Mild hypertension"
}

findings = "Patient shows elevated blood pressure 145/90, mild anxiety symptoms, Vitamin D deficiency, sedentary lifestyle."
parameters = "BP: 145/90, Vitamin D: 18 ng/mL, BMI: 27.4"
observations = "Mild stress, irregular sleep, low physical activity, healthy diet overall"

report = run_pipeline(user_profile, findings, parameters, observations)

print("\n📋 FINAL REPORT:")
print(report)