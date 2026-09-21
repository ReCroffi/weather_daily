import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from weather_daly.storage import load_to_postgres
from weather_daly.ingestion import fetch_weather_data


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None

if engine is None:
    print("DATABASE_URL não configurada. Defina a variável de ambiente antes de executar o pipeline.")
else:
    # Executar o pipeline de ingestão e carregamento de dados
    weather_data = fetch_weather_data(lat=-23.5505, lon=-46.6333, start_date="2021-01-01", end_date="2025-12-31")
    load_to_postgres(weather_data, engine)