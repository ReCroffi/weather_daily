# weather_daly

Terminei o pipeline preditivo do clima: previsão da temperatura máxima do dia seguinte a partir do clima de hoje, com coleta via Interface de Programação de Aplicações (API) pública, PostgreSQL (window functions pra feature engineering) e dois modelos do scikit-learn avaliados contra um baseline de persistência. Depois virou também um webapp simples mostrando a previsão mais recente.

## Resultado

RandomForestRegressor ficou com o menor erro: erro absoluto médio (MAE) de 1,84°C, contra 2,02°C da regressão linear e 2,30°C do baseline (usar a temperatura de hoje como previsão de amanhã, sem modelo nenhum). Os dois modelos batem o baseline — a complexidade extra do RandomForest valeu a pena nesse conjunto de dados.

Dados: 2021-01-01 até hoje, coordenadas de São Paulo (-23.5505, -46.6333) — a coleta busca a data mais recente disponível na Open-Meteo dinamicamente, sem data fixa cravada no código. Corte treino/teste em 2024-01-01, respeitando ordem cronológica — sem shuffle, é série temporal.

## Limitação

Isso não é previsão do tempo de um dia realmente desconhecido — é comparação retrospectiva (backtesting). `load_features` só aceita dias em que o `temp_max_dia_seguinte` já é conhecido, então todo dia que o pipeline "prevê" já tem o resultado real gravado no banco. É assim que dá pra calcular o MAE, mas também é por isso que não é previsão de verdade ainda. Falta o caminho pra prever um dia genuinamente futuro: pegar o dia mais recente sem exigir target, montar a linha de features dele, e rodar só `model.predict()`, sem MAE nenhum pra comparar.

## Pipeline

1. Coleta os dados históricos direto da Open-Meteo Archive API (sem chave, sem cadastro).
2. Carrega em `weather_daily` via upsert (`ON CONFLICT ... DO UPDATE`) — idempotente, rodar de novo não duplica nem quebra.
3. Explora com agregações nativas do Postgres (`STDDEV`, `CORR`, `EXTRACT`) direto no `psql`, sem passar pelo pandas.
4. Monta as features em `weather_features`, uma view com `LEAD()` pro target (temperatura de amanhã) e uma média móvel de 3 dias via `AVG() OVER (... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
5. Separa treino/teste por data, treina e avalia (MAE) `LinearRegression` e `RandomForestRegressor`, comparando os dois contra o baseline.
6. Grava cada previsão em `model_predictions` (data, modelo, valor real, valor previsto) — dá pra refazer a comparação inteira via Structured Query Language (SQL) pura depois, sem precisar do pandas.

## Webapp

Página simples (Flask + Jinja2, renderizado no servidor, sem JavaScript) mostrando a previsão mais recente direto do banco, pros três modelos lado a lado.

![Webapp weather_daly mostrando a previsão do dia](docs/screenshot-webapp.png)

## Setup

Ver [`docs/SETUP.md`](docs/SETUP.md) — Postgres via Docker e cheat sheet do `uv`.

## Estrutura

| Caminho | O quê | Fase correspondente no roteiro |
|---|---|---|
| `sql/schema.sql` | Data Definition Language (DDL) de `weather_daily` | 00 |
| `src/weather_daly/ingestion.py` | `fetch_weather_data` | 01 |
| `src/weather_daly/storage.py` | `load_to_postgres` (upsert), `ingest_results` (grava previsões), `get_latest_predictions` | 02, 08 |
| `sql/exploration.sql` | queries exploratórias | 03 |
| `sql/features_view.sql` | view com window functions | 04 |
| `src/weather_daly/modeling.py` | `load_features`, `split_train_test`, `baseline_predict`, `train_and_evaluate` | 05, 06, 07 |
| `sql/predictions_schema.sql` | DDL de `model_predictions` | 08 |
| `src/weather_daly/main.py` | orquestra o pipeline inteiro, ponta a ponta | — |
| `app.py` | webapp Flask, rota `/` renderiza a previsão mais recente | — |
| `templates/index.html` | template Jinja2 da página | — |
| `assets/css/styles.css` | estilo da página | — |

## Próximos passos

- Agendar (cron ou systemd timer) o `main.py` rodando sozinho todo dia, sem depender do meu PC.
- Previsão de um dia genuinamente futuro, não só backtesting (ver Limitação acima).
- Hospedar em algum lugar que rode Python de verdade (Render, Railway) — GitHub Pages só serve estático, não roda Flask nem fala com Postgres.
