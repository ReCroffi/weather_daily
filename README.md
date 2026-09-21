# weather_daly

Exercício de aquecimento: prever a temperatura máxima do dia seguinte a partir do clima de hoje, usando a API pública da Open-Meteo, PostgreSQL (com window functions) e scikit-learn.

Roteiro completo com o contrato de cada fase: [Pipeline Preditivo do Clima](https://claude.ai/artifact/2oM3KEn3EDayk6jSdpVcqw)

## Setup

Ver [`docs/SETUP.md`](docs/SETUP.md) — Postgres via Docker e cheat sheet do `uv`.

## Estrutura

| Caminho | O quê | Fase correspondente no roteiro |
|---|---|---|
| `sql/schema.sql` | DDL de `weather_daily` | 00 |
| `src/weather_daly/ingestion.py` | `fetch_weather_data` | 01 |
| `src/weather_daly/storage.py` | `load_to_postgres` (upsert) | 02 |
| `sql/exploration.sql` | queries exploratórias | 03 |
| `sql/features_view.sql` | view com window functions | 04 |
| `src/weather_daly/modeling.py` | `load_features`, `split_train_test`, `baseline_predict`, `train_and_evaluate` | 05, 06, 07 |
| `sql/predictions_schema.sql` | DDL de `model_predictions` | 08 |
| `src/weather_daly/evaluation.py` | comparação final | 08 |
