from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    name: str
    age: int
    gender: str
    occupation: Optional[str] = ""
    medical_history: Optional[str] = ""

class MedicalInput(BaseModel):
    user_profile: UserProfile
    findings: str
    parameters: Optional[str] = ""
    observations: Optional[str] = ""

class RiskIndicator(BaseModel):
    name: str
    level: str
    explanation: str

class WellnessReport(BaseModel):
    profile_summary: str
    key_observations: List[str]
    interpretations: List[str]
    risk_indicators: List[dict]
    wellness_insights: List[str]
    recommendations: List[str]
    lifestyle_suggestions: List[str]
    wellness_score: int