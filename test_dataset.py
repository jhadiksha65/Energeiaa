import time
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import run_pipeline

# Load dataset
df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")
print(f"✅ Dataset loaded! Total patients: {len(df)}")
print(f"📋 Columns: {list(df.columns)}\n")

# Track results
results = []

# Test first 3 patients
for i, row in df.head(3).iterrows():
    print(f"\n{'='*60}")
    print(f"🔍 Testing Patient {i+1} of 3")
    print(f"{'='*60}")
    print(f"Disease: {row.get('Disease', 'N/A')}")
    print(f"Age: {row.get('Age', 'N/A')} | Gender: {row.get('Gender', 'N/A')}")
    print(f"BP: {row.get('Blood Pressure', 'N/A')} | Cholesterol: {row.get('Cholesterol Level', 'N/A')}")

    user_profile = {
        "name": f"Patient {i+1}",
        "age": int(row.get("Age", 30)),
        "gender": str(row.get("Gender", "Unknown")),
        "occupation": "Not provided",
        "medical_history": str(row.get("Disease", "None"))
    }

    findings = f"""
    Disease: {row.get('Disease', 'N/A')}
    Fever: {row.get('Fever', 'N/A')}
    Cough: {row.get('Cough', 'N/A')}
    Fatigue: {row.get('Fatigue', 'N/A')}
    Difficulty Breathing: {row.get('Difficulty Breathing', 'N/A')}
    """

    parameters = f"Blood Pressure: {row.get('Blood Pressure', 'N/A')}, Cholesterol: {row.get('Cholesterol Level', 'N/A')}"
    observations = f"Age: {row.get('Age')}, Gender: {row.get('Gender')}, Outcome: {row.get('Outcome Variable', 'N/A')}"

    try:
        report = run_pipeline(user_profile, findings, parameters, observations)

        # Store result
        results.append({
            "patient": i + 1,
            "disease": row.get('Disease', 'N/A'),
            "wellness_score": report['wellness_score'],
            "risks": [r['name'] for r in report['risk_indicators']]
        })

        # Print results
        print(f"\n✅ Pipeline complete for Patient {i+1}!")
        print(f"🏆 Wellness Score : {report['wellness_score']}/100")

        if report['wellness_score'] >= 75:
            print(f"💚 Status         : Great Health")
        elif report['wellness_score'] >= 50:
            print(f"💛 Status         : Fair Health")
        else:
            print(f"❤️  Status         : Needs Attention")

        print(f"\n📋 Profile Summary:")
        print(f"   {report['profile_summary']}")

        print(f"\n🔍 Key Observations:")
        for obs in report['key_observations']:
            print(f"   • {obs}")

        print(f"\n⚠️  Risk Indicators:")
        for risk in report['risk_indicators']:
            print(f"   • {risk['name']} → {risk['level']}")

        print(f"\n✅ Top Recommendations:")
        for rec in report['recommendations'][:3]:
            print(f"   • {rec}")

    except Exception as e:
        print(f"❌ Error for Patient {i+1}: {e}")
        results.append({
            "patient": i + 1,
            "disease": row.get('Disease', 'N/A'),
            "wellness_score": "Error",
            "risks": []
        })

    # Wait between patients to avoid rate limits
    if i < 2:
        print(f"\n⏳ Waiting 5 seconds before next patient...")
        time.sleep(5)

# Final summary
print(f"\n{'='*60}")
print(f"📊 FINAL SUMMARY")
print(f"{'='*60}")
for r in results:
    score = r['wellness_score']
    status = "✅ Great" if score != "Error" and score >= 75 else "⚠️ Fair" if score != "Error" and score >= 50 else "❌ Needs Attention" if score != "Error" else "💥 Error"
    print(f"Patient {r['patient']} | {r['disease']:<30} | Score: {str(score):<5} | {status}")

print(f"\n🎉 Dataset testing complete!")