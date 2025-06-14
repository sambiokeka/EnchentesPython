from flask import Flask, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "enchentes_BD"
}

def conectar_mysql():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    local = request.form.get("local")
    nivel_agua = request.form.get("nivel_agua")
    pessoas_afetadas = request.form.get("pessoas_afetadas")
    data_enchente = request.form.get("data_enchente")

    try:
        nivel_agua = float(nivel_agua) if nivel_agua else None
    except ValueError:
        nivel_agua = None

    try:
        pessoas_afetadas = int(pessoas_afetadas) if pessoas_afetadas else None
    except ValueError:
        pessoas_afetadas = None

    conn = conectar_mysql()
    cursor = conn.cursor()
    query = """
        INSERT INTO registros (local, nivel_agua, pessoas_afetadas, data_enchente)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (local, nivel_agua, pessoas_afetadas, data_enchente))
    conn.commit()
    cursor.close()
    conn.close()
    return "Ocorrência cadastrada com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)