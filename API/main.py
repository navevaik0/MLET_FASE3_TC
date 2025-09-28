import os
import sqlite3
import pandas as pd
from fastapi import FastAPI
from kaggle.api.kaggle_api_extended import KaggleApi

# Configuração do Kaggle
os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\erick\Documents\FIAP\TC\FASE3_TC\kaggle"

app = FastAPI(
    title="Titanic Dataset Loader",
    description="API que baixa o dataset Titanic do Kaggle e salva em um banco SQLite local",
    version="1.0.0"
)

# Estrutura de pastas
RAW_FOLDER = os.path.join("FASE3_TC", "data", "RAW")
PROCESSED_FOLDER = os.path.join("FASE3_TC", "data", "PROCESSED")

DATASET_FILE = os.path.join(RAW_FOLDER, "Titanic-Dataset.csv")
DB_FILE = os.path.join(PROCESSED_FOLDER, "titanic.db")
KAGGLE_DATASET = "yasserh/Titanic-Dataset"

def download_dataset():
    """Baixa o dataset Titanic e salva em data/RAW"""
    os.makedirs(RAW_FOLDER, exist_ok=True)
    if not os.path.exists(DATASET_FILE):
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(KAGGLE_DATASET, path=RAW_FOLDER, unzip=True)
        # Renomeia se necessário
        raw_file = os.path.join(RAW_FOLDER, "titanic.csv")
        if os.path.exists(raw_file):
            os.rename(raw_file, DATASET_FILE)
    return DATASET_FILE

def init_db():
    """Cria o banco SQLite em data/PROCESSED a partir do CSV"""
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    if not os.path.exists(DB_FILE):
        csv_path = download_dataset()
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(DB_FILE)
        df.to_sql("titanic", conn, if_exists="replace", index=False)
        conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {
        "message": "Dataset Titanic salvo com sucesso!",
        "csv_path": DATASET_FILE,
        "db_path": DB_FILE
    }