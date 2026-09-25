# weather_daly

[Português](README.md) | **English**

A predictive weather pipeline: it forecasts tomorrow's maximum temperature from today's weather, with data collected from a public API, PostgreSQL (window functions for feature engineering) and two scikit-learn models evaluated against a persistence baseline. It later grew a simple webapp that shows the latest prediction.

## Results

RandomForestRegressor had the lowest error: a mean absolute error (MAE) of 2.17°C, versus 2.19°C for linear regression and 2.30°C for the baseline (using today's temperature as tomorrow's forecast, no model at all). Both models beat the baseline, but only by about 6%. With four variables from today, that's what the data gives, and it's an honest number.

Data: 2021-01-01 to today, São Paulo coordinates (-23.5505, -46.6333). Collection fetches the most recent date available on Open-Meteo dynamically, with no hardcoded end date. Train/test split at 2024-01-01, in chronological order and without shuffling, since this is a time series.

## Correction: data leakage (the original number was wrong)

The first version of this README reported an MAE of **1.84°C** for RandomForest and 2.02°C for linear regression, beating the baseline by 20%. That number wasn't real.

The `weather_features` view builds four columns with `LEAD()`: `temp_max_dia_seguinte` (the target), plus `temp_min_dia_seguinte`, `precipitacao_dia_seguinte` and `velocidade_vento_dia_seguinte`. `split_train_test` only removed the target from the features, so the other three went into training. In other words, the model used **tomorrow's** minimum temperature, rain and wind to predict **tomorrow's** maximum. That's data leakage: information that doesn't exist at prediction time.

The fix drops every column ending in `_dia_seguinte` from the features (only the target stays, as `y`). Honest results:

| Model | MAE with leakage | MAE fixed |
|---|---|---|
| RandomForestRegressor | 1.84°C | **2.17°C** |
| LinearRegression | 2.02°C | **2.19°C** |
| Baseline (persistence) | 2.30°C | 2.30°C |

RandomForest also got `random_state=42`, so the number is reproducible across runs.

## Limitation

This still isn't a forecast for a truly unknown day: it's a retrospective comparison (backtesting). `load_features` only accepts days whose `temp_max_dia_seguinte` is already known, so every day the pipeline "predicts" already has the real outcome stored in the database. That's what makes computing the MAE possible.

With the leak fixed, the path to a genuinely future forecast is open: the features now come from today only, so it's a matter of taking the most recent day without requiring a target, building its feature row and running `model.predict()`. Before the fix that wasn't even possible, because the model depended on columns that only exist tomorrow. That was the symptom that should have tipped me off sooner.

## Pipeline

1. Pulls historical data straight from the Open-Meteo Archive API (no key, no sign-up).
2. Loads it into `weather_daily` via upsert (`ON CONFLICT ... DO UPDATE`). It's idempotent: running it again doesn't duplicate or break anything.
3. Explores it with native Postgres aggregations (`STDDEV`, `CORR`, `EXTRACT`) directly in `psql`, without going through pandas.
4. Builds the features in `weather_features`, a view with `LEAD()` for the target (tomorrow's temperature) and a 3-day moving average via `AVG() OVER (... ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
5. Splits train/test by date, drops every next-day column from the features (only the target stays), trains and evaluates (MAE) `LinearRegression` and `RandomForestRegressor`, and compares both against the baseline.
6. Stores every prediction in `model_predictions` (date, model, actual value, predicted value), so the whole comparison can be redone later in plain SQL, without pandas.

## Webapp

A simple page (Flask + Jinja2, server-side rendered, no JavaScript) showing the latest prediction straight from the database, with the three models side by side.

![weather_daly webapp showing the day's prediction](docs/screenshot-webapp.png)

## Setup

See [`docs/SETUP.md`](docs/SETUP.md) (in Portuguese): Postgres via Docker and a `uv` cheat sheet. Short version:

```
docker run --name pg-clima -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
cp .env.example .env
uv sync
uv run python -m weather_daly.main
uv run flask run
```

The SQL files in `sql/` need to be applied to the database before the first run (`schema.sql`, `features_view.sql`, `predictions_schema.sql`).

## Structure

Column and table names are in Portuguese: `dia` = day, `temp_max`/`temp_min` = max/min temperature, `precipitacao` = precipitation, `velocidade_vento` = wind speed, `_dia_seguinte` = next day.

| Path | What | Matching phase in the roadmap |
|---|---|---|
| `sql/schema.sql` | DDL for `weather_daily` | 00 |
| `src/weather_daly/ingestion.py` | `fetch_weather_data` | 01 |
| `src/weather_daly/storage.py` | `load_to_postgres` (upsert), `ingest_results` (stores predictions), `get_latest_predictions` | 02, 08 |
| `sql/exploration.sql` | exploratory queries | 03 |
| `sql/features_view.sql` | view with window functions | 04 |
| `src/weather_daly/modeling.py` | `load_features`, `split_train_test`, `baseline_predict`, `train_and_evaluate` | 05, 06, 07 |
| `sql/predictions_schema.sql` | DDL for `model_predictions` | 08 |
| `src/weather_daly/main.py` | runs the whole pipeline end to end | n/a |
| `app.py` | Flask webapp, the `/` route renders the latest prediction | n/a |
| `templates/index.html` | Jinja2 page template | n/a |
| `assets/css/styles.css` | page styles | n/a |

## Next steps

- Schedule `main.py` (cron or a systemd timer) to run on its own every day, without depending on my PC.
- Forecast a genuinely future day, not just backtesting (see Limitation above).
- Host it somewhere that actually runs Python (Render, Railway). GitHub Pages only serves static files; it can't run Flask or talk to Postgres.
