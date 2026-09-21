from sqlalchemy import text
import pandas as pd 

def load_to_postgres(df: pd.DataFrame, engine) -> None:
    df = df.rename(columns={"time": "dia", "temperature_2m_max": "temp_max", "temperature_2m_min": "temp_min", "precipitation_sum": "precipitacao", "windspeed_10m_max": "velocidade_vento" })
    df_dict = df.to_dict(orient="records")
    with engine.connect() as connection:
        connection.execute(text("INSERT INTO weather_daily (dia, temp_max, temp_min, precipitacao, velocidade_vento) VALUES (:dia, :temp_max, :temp_min, :precipitacao, :velocidade_vento) ON CONFLICT (dia) DO UPDATE SET temp_max = EXCLUDED.temp_max, temp_min = EXCLUDED.temp_min, precipitacao = EXCLUDED.precipitacao, velocidade_vento = EXCLUDED.velocidade_vento", df_dict))
        connection.commit()
