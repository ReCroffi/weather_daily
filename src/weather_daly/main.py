import os
from datetime import datetime

from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sqlalchemy import create_engine

from weather_daly.ingestion import fetch_weather_data
from weather_daly.modeling import (
    baseline_predict,
    load_features,
    split_train_test,
    train_and_evaluate,
)
from weather_daly.storage import ingest_results, load_to_postgres

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None

if engine is None:
    print("DATABASE_URL não configurada. Defina a variável de ambiente antes de executar o pipeline.")
else:
    # Executar o pipeline de ingestão e carregamento de dados
    weather_data = fetch_weather_data(lat=-23.5505, lon=-46.6333, start_date="2021-01-01", end_date="2025-12-31")
    load_to_postgres(weather_data, engine)
    model = [("RandomForestRegressor", RandomForestRegressor()), ("LinearRegression", LinearRegression())]
    loaded_features = load_features(engine)
    cutoff_date = "2024-01-01"
    cutoff_date = datetime.strptime(cutoff_date, "%Y-%m-%d").date()  # noqa: DTZ007
    X_train, X_test, y_train, y_test, dia_test = split_train_test(loaded_features, cutoff_date)
    baseline_predictions = baseline_predict(X_test)  
    mae_baseline = mean_absolute_error(y_test, baseline_predictions)
    resultados = {}   
    for model_name, model_instance in model:
        mae, predictions = train_and_evaluate(X_train, X_test, y_train, y_test, model_instance)
        resultados[model_name] = {"MAE": mae, "predictions": predictions}
    resultados["Baseline"] = {"MAE": mae_baseline, "predictions": baseline_predictions}
    
    for model_name, result in resultados.items():
        ingest_results(model_name, result["predictions"], y_test, dia_test, engine)
    