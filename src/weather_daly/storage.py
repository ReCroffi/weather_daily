import pandas as pd
from sqlalchemy import text


def load_to_postgres(df: pd.DataFrame, engine) -> None:
    df = df.rename(columns={"time": "dia", "temperature_2m_max": "temp_max", "temperature_2m_min": "temp_min", "precipitation_sum": "precipitacao", "windspeed_10m_max": "velocidade_vento" })
    df_dict = df.to_dict(orient="records")
    with engine.connect() as connection:
        connection.execute(text("INSERT INTO weather_daily (dia, temp_max, temp_min, precipitacao, velocidade_vento) VALUES (:dia, :temp_max, :temp_min, :precipitacao, :velocidade_vento) ON CONFLICT (dia) DO UPDATE SET temp_max = EXCLUDED.temp_max, temp_min = EXCLUDED.temp_min, precipitacao = EXCLUDED.precipitacao, velocidade_vento = EXCLUDED.velocidade_vento"), df_dict)
        connection.commit()

def ingest_results(model_name, predictions, y_test, dia_test, engine) -> None:
    """
    Insere os resultados das previsões do modelo no banco de dados PostgreSQL.

    Args:
        model_name (str): Nome do modelo.
        predictions (np.ndarray): Previsões do modelo.
        y_test (pd.Series): Valores reais do conjunto de teste.
        dia_test (pd.Series): Datas correspondentes ao conjunto de teste.
        engine: Objeto SQLAlchemy Engine para conexão com o banco de dados.
    """
    results_df = pd.DataFrame({
        "dia": dia_test,
        "modelo": model_name,
        "valor_real": y_test,
        "valor_previsto": predictions
    })

    results_dict = results_df.to_dict(orient="records")
    with engine.connect() as connection:
        connection.execute(text("INSERT INTO model_predictions (dia, modelo, valor_real, valor_previsto) VALUES (:dia, :modelo, :valor_real, :valor_previsto) ON CONFLICT (dia, modelo) DO UPDATE SET valor_real = EXCLUDED.valor_real, valor_previsto = EXCLUDED.valor_previsto"), results_dict)
        connection.commit()