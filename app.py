from flask import Flask, render_template
from weather_daly.storage import get_latest_predictions
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder="assets", static_url_path="/assets")

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None


@app.route("/")
def funciona():
    if engine is None:
        return "DATABASE_URL não configurada. Defina a variável de ambiente antes de executar o pipeline."
    latest_predictions = get_latest_predictions(engine)
    if not latest_predictions:
        return "Nenhuma previsão encontrada no banco de dados."
    print(f"Últimas previsões: {latest_predictions}")
    return render_template("index.html", previsoes=latest_predictions, dia_previsto=latest_predictions[0]['dia'])    

if __name__ == "__main__":
    app.run(debug=True)