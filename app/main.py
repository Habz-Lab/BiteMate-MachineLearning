from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.model.model import predict_nutriscore

app = FastAPI()
class NutritionIn(BaseModel):
    takaran_saji: float
    energi: float
    protein: float
    lemak: float
    # karbohidrat: float
    serat: float
    natrium: float
    gula: float

class PredictionOut(BaseModel):
    score: str
    cal_per_100g: int

@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/predict", response_model=PredictionOut)
def predict(payload: NutritionIn):
    try:
        # Convert the nutrients to per 100g basis
        energi_per_100g = payload.energi * 100 / payload.takaran_saji
        protein_per_100g = payload.protein * 100 / payload.takaran_saji
        # karbohidrat_per_100g = payload.karbohidrat * 100 / payload.takaran_saji
        serat_per_100g = payload.serat * 100 / payload.takaran_saji
        natrium_per_100g = payload.natrium * 100 / payload.takaran_saji
        lemak_per_100g = payload.lemak * 100 / payload.takaran_saji
        gula_per_100g = payload.gula * 100 / payload.takaran_saji

        # Calculate Nutri-Score
        score = predict_nutriscore(energi_per_100g,
                                   protein_per_100g,
                                   lemak_per_100g,
                                #    karbohidrat_per_100g,
                                   serat_per_100g,
                                   natrium_per_100g,
                                   gula_per_100g)

        # Return the Nutri-Score and calories per 100g
        return {"score": score, "cal_per_100g": round(energi_per_100g)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))