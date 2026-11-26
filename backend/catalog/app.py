

from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

# Base de datos exclusiva de Catalog
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "catalog.db")


def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


# Crear tabla e inventario inicial
def inicializar_db():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    total = conexion.execute(
        "SELECT COUNT(*) FROM inventario"
    ).fetchone()[0]

    if total == 0:
        recursos = [
            ("Contenedor refrigerado", "Contenedores", 25, "Disponible"),
            ("Grúa portuaria", "Maquinaria", 5, "Operativa"),
            ("Espacio de almacenamiento", "Almacenamiento", 100, "Disponible")
        ]

        conexion.executemany("""
            INSERT INTO inventario
            (nombre, categoria, cantidad, estado)
            VALUES (?, ?, ?, ?)
        """, recursos)

    conexion.commit()
    conexion.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "servicio": "Catalog",
        "estado": "activo"
    }), 200


# Consultar inventario
@app.route("/inventario", methods=["GET"])
def obtener_inventario():
    conexion = conectar()
    recursos = conexion.execute(
        "SELECT * FROM inventario"
    ).fetchall()
    conexion.close()

    return jsonify([dict(recurso) for recurso in recursos]), 200


# Agregar un recurso
@app.route("/inventario", methods=["POST"])
def agregar_recurso():
    datos = request.get_json()

    if not datos or not datos.get("nombre"):
        return jsonify({
            "error": "El nombre del recurso es obligatorio"
        }), 400

    try:
        cantidad = int(datos.get("cantidad", 0))
        if cantidad < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            "error": "La cantidad debe ser un número entero no negativo"
        }), 400

    nombre = datos["nombre"]
    categoria = datos.get("categoria", "General")
    estado = datos.get("estado", "Disponible")

    conexion = conectar()

    cursor = conexion.execute("""
        INSERT INTO inventario
        (nombre, categoria, cantidad, estado)
        VALUES (?, ?, ?, ?)
    """, (nombre, categoria, cantidad, estado))

    conexion.commit()

    recurso = conexion.execute(
        "SELECT * FROM inventario WHERE id = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conexion.close()

    return jsonify({
        "mensaje": "Recurso agregado correctamente",
        "recurso": dict(recurso)
    }), 201


if __name__ == "__main__":
    inicializar_db()
    app.run(host="127.0.0.1", port=5002, debug=True)
