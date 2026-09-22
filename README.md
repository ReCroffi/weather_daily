# weather_daly

Terminei o pipeline preditivo do clima: previsão da temperatura máxima do dia seguinte a partir do clima de hoje, com coleta via Interface de Programação de Aplicações (API) pública, PostgreSQL (window functions pra feature engineering) e dois modelos do scikit-learn avaliados contra um baseline de persistência.

## Resultado

RandomForestRegressor ficou com o menor erro: erro absoluto médio (MAE) de 1,84°C, contra 2,02°C da regressão linear e 2,30°C do baseline (usar a temperatura de hoje como previsão de amanhã, sem modelo nenhum). Os dois modelos batem o baseline — a complexidade extra do RandomForest valeu a pena nesse conjunto de dados.

Dados: 1.826 dias (2021-01-01 a 2025-12-31), coordenadas de São Paulo (-23.5505, -46.6333). Corte treino/teste em 2024-01-01, respeitando ordem cronológica — sem shuffle, é série temporal.

## Pipeline

1. Coleta os dados históricos direto da Open-Meteo Archive API (sem chave, sem cadastro).
2. Carrega em `weather_daily` via upsert (`ON CONFLICT ... DO UPDATE`) — idempotente, rodar de novo não duplica nem quebra.
3. Explora com agregações nativas do Postgres (`STDDEV`, `CORR`, `EXTRACT`) direto no `psql`, sem passar pelo pandas.
4. Monta as features em `weather_features`, uma view com `LEAD()` pro target (temperatura de amanhã) e uma média móvel de 3 dias via `AVG() OVER (... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
5. Separa treino/teste por data, treina e avalia (MAE) `LinearRegression` e `RandomForestRegressor`, comparando os dois contra o baseline.
6. Grava cada previsão em `model_predictions` (data, modelo, valor real, valor previsto) — dá pra refazer a comparação inteira via Structured Query Language (SQL) pura depois, sem precisar do pandas.

## Setup

Ver [`docs/SETUP.md`](docs/SETUP.md) — Postgres via Docker e cheat sheet do `uv`.

## Estrutura

| Caminho | O quê | Fase correspondente no roteiro |
|---|---|---|
| `sql/schema.sql` | Data Definition Language (DDL) de `weather_daily` | 00 |
| `src/weather_daly/ingestion.py` | `fetch_weather_data` | 01 |
| `src/weather_daly/storage.py` | `load_to_postgres` (upsert), `ingest_results` (grava previsões) | 02, 08 |
| `sql/exploration.sql` | queries exploratórias | 03 |
| `sql/features_view.sql` | view com window functions | 04 |
| `src/weather_daly/modeling.py` | `load_features`, `split_train_test`, `baseline_predict`, `train_and_evaluate` | 05, 06, 07 |
| `sql/predictions_schema.sql` | DDL de `model_predictions` | 08 |
| `src/weather_daly/main.py` | orquestra o pipeline inteiro, ponta a ponta | — |

## Próximo passo

Webapp simples (Flask + Jinja2, renderizado no servidor, sem JavaScript) mostrando a previsão mais recente direto do banco.
