from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np
import random

app = FastAPI()

# Carrega modelo
model = joblib.load("modelo/modelo_final.pkl")

# Configura templates
templates = Jinja2Templates(directory="templates")

# Features usadas no modelo
FEATURES = ["Pclass", "Age", "SibSp", "Parch", "Fare", "Sex_male", "Embarked_C", "Embarked_Q", "Embarked_S"]

def generate_random_passenger():
    return {
        "Pclass": random.choice([1, 2, 3]),
        "Age": round(random.uniform(1, 80), 1),
        "SibSp": random.randint(0, 3),
        "Parch": random.randint(0, 3),
        "Fare": round(random.uniform(5, 100), 2),
        "Sex_male": random.choice([0, 1]),
        "Embarked_C": random.choice([0, 1]),
        "Embarked_Q": random.choice([0, 1]),
        "Embarked_S": random.choice([0, 1])
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("simulator.html", {"request": request})

@app.get("/simulate")
def simulate_passenger():
    passenger = generate_random_passenger()
    input_data = np.array([[passenger[feature] for feature in FEATURES]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    return {
        "survived": bool(prediction),
        "probability": round(probability, 3),
        "passenger_profile": passenger
    }