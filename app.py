from flask import Flask

app = Flask(__name__)

@app.route("/")
def funciona():
    return "Funcionando!"


if __name__ == "__main__":
    app.run(debug=True)