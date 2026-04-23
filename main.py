from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from models.schemas import MedicalInput
from agents.orchestrator import run_pipeline
import os
import shutil
import pandas as pd

load_dotenv()

app = FastAPI(title="Energeiaa Wellness AI")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "message": "Energeiaa is running"})

@app.post("/generate-report")
async def generate_report(data: MedicalInput):
    try:
        report = run_pipeline(
            user_profile=data.user_profile.dict(),
            findings=data.findings,
            parameters=data.parameters,
            observations=data.observations
        )
        return JSONResponse({"success": True, "report": report})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/report")
async def report_page(request: Request):
    return templates.TemplateResponse(request=request, name="report.html")

@app.get("/dataset")
async def dataset_page(request: Request):
    return templates.TemplateResponse(request=request, name="dataset.html")

@app.get("/dataset-patients")
async def get_patients():
    try:
        df = pd.read_csv("Disease_symptom_and_patient_profile_dataset.csv")
        patients = df.head(10).to_dict(orient="records")
        return JSONResponse({"success": True, "patients": patients, "total": len(df)})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})

@app.post("/run-dataset-patient")
async def run_dataset_patient(data: dict):
    try:
        row = data.get("patient", {})
        user_profile = {
            "name": f"Patient {data.get('index', 1)}",
            "age": int(row.get("Age", 30)),
            "gender": str(row.get("Gender", "Unknown")),
            "occupation": "Not provided",
            "medical_history": str(row.get("Disease", "None"))
        }
        findings = f"Disease: {row.get('Disease','N/A')}, Fever: {row.get('Fever','N/A')}, Cough: {row.get('Cough','N/A')}, Fatigue: {row.get('Fatigue','N/A')}, Difficulty Breathing: {row.get('Difficulty Breathing','N/A')}"
        parameters = f"Blood Pressure: {row.get('Blood Pressure','N/A')}, Cholesterol: {row.get('Cholesterol Level','N/A')}"
        observations = f"Age: {row.get('Age')}, Gender: {row.get('Gender')}, Outcome: {row.get('Outcome Variable','N/A')}"

        report = run_pipeline(user_profile, findings, parameters, observations)
        return JSONResponse({"success": True, "report": report})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})

@app.post("/extract-prescription")
async def extract_prescription(file: UploadFile = File(...)):
    try:
        # Save uploaded image temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text using OCR agent
        from utils.ocr_agent import extract_text_from_image
        extracted_text = extract_text_from_image(temp_path)

        # Delete temp file
        os.remove(temp_path)

        return JSONResponse({
            "success": True,
            "extracted_text": extracted_text
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        })
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))