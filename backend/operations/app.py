

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "operations.db")


def conectar_db():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tablas():
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Tabla existente: conserva las operaciones registradas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            buque TEXT NOT NULL,
            contenedores INTEGER NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    # Nueva tabla para liberaciones aduaneras
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS liberaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenedor TEXT NOT NULL,
            agente_aduanal TEXT NOT NULL,
            estado TEXT NOT NULL,
            observaciones TEXT
        )
    """)

    conexion.commit()
    conexion.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "servicio": "Operations",
        "estado": "activo"
    }), 200


@app.route("/operaciones", methods=["GET"])
def obtener_operaciones():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM operaciones ORDER BY id DESC")
    operaciones = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()
    return jsonify(operaciones), 200


@app.route("/operaciones", methods=["POST"])
def registrar_operacion():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Se requieren datos JSON"}), 400

    tipo = datos.get("tipo")
    buque = datos.get("buque")
    contenedores = datos.get("contenedores")
    estado = datos.get("estado", "Programada")

    if not tipo or not buque or contenedores is None:
        return jsonify({
            "error": "El tipo, buque y contenedores son obligatorios"
        }), 400

    try:
        contenedores = int(contenedores)

        if contenedores <= 0:
            return jsonify({
                "error": "La cantidad debe ser mayor que cero"
            }), 400

        conexion = conectar_db()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO operaciones (tipo, buque, contenedores, estado)
            VALUES (?, ?, ?, ?)
        """, (tipo, buque, contenedores, estado))

        conexion.commit()
        nuevo_id = cursor.lastrowid
        conexion.close()

        return jsonify({
            "mensaje": "Operación registrada correctamente",
            "id": nuevo_id
        }), 201

    except ValueError:
        return jsonify({
            "error": "Los contenedores deben ser un número"
        }), 400


# Registrar una nueva liberación aduanera
@app.route("/liberaciones", methods=["POST"])
def registrar_liberacion():
    datos = request.get_json(silent=True)

    if not datos:
        return jsonify({"error": "Se requieren datos JSON"}), 400

    contenedor = datos.get("contenedor")
    agente = datos.get("agente_aduanal")
    estado = datos.get("estado", "Pendiente")
    observaciones = datos.get("observaciones", "")

    if not contenedor or not agente:
        return jsonify({
            "error": "El contenedor y el agente aduanal son obligatorios"
        }), 400

    if estado not in ["Pendiente", "En revisión", "Liberado", "Rechazado"]:
        return jsonify({"error": "Estado de liberación no válido"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO liberaciones
        (contenedor, agente_aduanal, estado, observaciones)
        VALUES (?, ?, ?, ?)
    """, (contenedor, agente, estado, observaciones))

    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()

    return jsonify({
        "mensaje": "Liberación aduanera registrada correctamente",
        "id": nuevo_id
    }), 201


# Consultar todas las liberaciones aduaneras
@app.route("/liberaciones", methods=["GET"])
def obtener_liberaciones():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM liberaciones ORDER BY id DESC")
    liberaciones = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()
    return jsonify(liberaciones), 200


if __name__ == "__main__":
    crear_tablas()
    app.run(host="127.0.0.1", port=5003, debug=True)

