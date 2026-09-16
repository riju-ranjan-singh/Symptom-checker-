import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# Mount the static directory to serve the frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

class SymptomRequest(BaseModel):
    symptoms: str

@app.post("/predict")
def predict(req: SymptomRequest):
    symptoms = req.symptoms
    if not symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms cannot be empty.")
        
    prompt = f"""
You are an expert AI medical assistant. A patient reports the following input:
"{symptoms}"

First, determine if this input describes a medical symptom, health condition, or injury.
If it is NOT a medical symptom (for example, a greeting, a name, or random text), you MUST output exactly this JSON:
{{
    "predicted_disease": "Invalid Input",
    "analysis": "This does not appear to be a medical symptom. Please describe your health symptoms.",
    "recommended_doctors": [],
    "home_remedies": []
}}

If it IS a medical symptom, carefully read and comprehend the text. Note any negations (e.g. "no fever").
Determine the most likely condition and output a valid JSON object.
Format:
{{
    "predicted_disease": "Name of the disease",
    "analysis": "Detailed explanation of why you suspect this, taking into account the context provided by the patient.",
    "recommended_doctors": ["Doctor Type 1", "Doctor Type 2"],
    "home_remedies": ["Remedy 1", "Remedy 2"]
}}
"""
    try:
        ollama_url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": "qwen2.5:0.5b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.3
            }
        }
        response = requests.post(ollama_url, json=payload, timeout=300)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")
            
        ai_text = response.json().get("response", "")
        data = json.loads(ai_text)
        
        return {
            "predicted_disease": data.get("predicted_disease", "Unknown"),
            "analysis": data.get("analysis", "No analysis provided."),
            "recommended_doctors": data.get("recommended_doctors", []),
            "home_remedies": data.get("home_remedies", [])
        }
        
    except json.JSONDecodeError:
        print("Failed to parse LLM output as JSON:", ai_text)
        return {
            "predicted_disease": "Analysis Completed",
            "analysis": ai_text,
            "recommended_doctors": ["General Physician"],
            "home_remedies": ["Please consult a doctor for a proper diagnosis."]
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to AI backend. Make sure it is running. Error: {str(e)}")

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
