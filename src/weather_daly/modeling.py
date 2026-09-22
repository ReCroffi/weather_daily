import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


def load_features(engine) -> pd.DataFrame:
    """
    Carrega os dados de features do banco de dados PostgreSQL.

    Args:
        engine: Objeto SQLAlchemy Engine para conexão com o banco de dados.

    Returns:
        pd.DataFrame: DataFrame contendo os dados de features.
    """
    query = "SELECT * FROM weather_features WHERE temp_max_dia_seguinte IS NOT NULL"
    return pd.read_sql(query, engine)


def split_train_test(df, cutoff_date) -> tuple:
    """
    Divide os dados em conjuntos de treino e teste com base na data de corte.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados de features.
        cutoff_date (str): Data de corte no formato 'YYYY-MM-DD'.

    Returns:
        tuple: Conjuntos de treino e teste (X_train, X_test, y_train, y_test).
    """
    train_df = df[df['dia'] < cutoff_date]
    test_df = df[df['dia'] >= cutoff_date]

    X_train = train_df.drop(columns=['temp_max_dia_seguinte', 'dia'])
    y_train = train_df['temp_max_dia_seguinte']
    X_test = test_df.drop(columns=['temp_max_dia_seguinte', 'dia'])
    y_test = test_df['temp_max_dia_seguinte']

    return X_train, X_test, y_train, y_test

def baseline_predict(X_test) -> np.ndarray:
    """
    Gera previsões de baseline para o conjunto de teste.

    Args:
        X_test (pd.DataFrame): Conjunto de teste contendo as features.

    Returns:
       np.ndarray: Previsões de baseline (média da temperatura máxima do dia anterior).
    """
    return X_test['temp_max'].values


def train_and_evaluate(X_train, X_test, y_train, y_test, model) -> float:
    """
    Treina um modelo de regressão linear e avalia seu desempenho.

    Args:
        X_train (pd.DataFrame): Conjunto de treino contendo as features.
        X_test (pd.DataFrame): Conjunto de teste contendo as features.
        y_train (pd.Series): Valores reais do conjunto de treino.
        y_test (pd.Series): Valores reais do conjunto de teste.

    Returns:
        float: Métricas de avaliação do modelo (MAE).
    """


    
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    
    mae = mean_absolute_error(y_test, predictions)

    return mae