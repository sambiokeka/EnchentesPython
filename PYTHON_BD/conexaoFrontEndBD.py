from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

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
    cidade = request.form.get("cidade")
    nivel_agua = request.form.get("nivel_agua")
    pessoas_afetadas = request.form.get("pessoas_afetadas")
    data_enchente = request.form.get("data_enchente")

    conn = conectar_mysql()
    cursor = conn.cursor()
    query = """
        INSERT INTO registros (cidade, nivel_agua, pessoas_afetadas, data_enchente)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (cidade, nivel_agua, pessoas_afetadas, data_enchente))
    conn.commit()
    cursor.close()
    conn.close()
    return "Ocorrência cadastrada com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)