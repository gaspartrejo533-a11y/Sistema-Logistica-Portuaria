

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
import sqlite3
import os

app = Flask(__name__)

# Configuracion del servicio Auth
app.config["SECRET_KEY"] = os.environ["AUTH_SECRET_KEY"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "auth.db")

serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_db():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            rol TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute(
        "SELECT id FROM usuarios WHERE correo = ?",
        ("admin@puerto.com",)
    )

    admin = cursor.fetchone()

    if not admin:
        password = os.environ.get(
            "ADMIN_PASSWORD",
            "PuertoAdmin2026!"
        )

        cursor.execute("""
            INSERT INTO usuarios
            (nombre, correo, rol, password_hash)
            VALUES (?, ?, ?, ?)
        """, (
            "Administrador",
            "admin@puerto.com",
            "admin",
            generate_password_hash(password)
        ))

    conexion.commit()
    conexion.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "servicio": "Auth",
        "estado": "activo"
    })


@app.route("/usuarios", methods=["POST"])
def registrar_usuario():
    datos = request.get_json(silent=True) or {}

    nombre = datos.get("nombre")
    correo = datos.get("correo")
    password = datos.get("password")
    rol = datos.get("rol", "operador")

    if not nombre or not correo or not password:
        return jsonify({
            "error": "Faltan datos obligatorios"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "La contraseÃ±a debe tener al menos 8 caracteres"
        }), 400

    roles_permitidos = [
        "operador",
        "agente_aduanal",
        "transportista"
    ]

    if rol not in roles_permitidos:
        return jsonify({
            "error": "Rol no permitido"
        }), 400

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios
            (nombre, correo, rol, password_hash)
            VALUES (?, ?, ?, ?)
        """, (
            nombre,
            correo,
            rol,
            generate_password_hash(password)
        ))

        conexion.commit()

        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "El correo ya estÃ¡ registrado"
        }), 409

    finally:
        conexion.close()


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json(silent=True) or {}

    correo = datos.get("correo")
    password = datos.get("password")

    if not correo or not password:
        return jsonify({
            "error": "Correo y contraseÃ±a son obligatorios"
        }), 400

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE correo = ?",
        (correo,)
    )

    usuario = cursor.fetchone()
    conexion.close()

    if not usuario or not check_password_hash(
        usuario["password_hash"], password
    ):
        return jsonify({
            "error": "Credenciales incorrectas"
        }), 401

    datos_usuario = {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    }

    token = serializer.dumps(datos_usuario)

    return jsonify({
        "mensaje": "Inicio de sesiÃ³n exitoso",
        "token": token,
        "usuario": datos_usuario
    })


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, correo, rol
        FROM usuarios
        ORDER BY id
    """)

    usuarios = [
        dict(usuario) for usuario in cursor.fetchall()
    ]

    conexion.close()

    return jsonify(usuarios)


if __name__ == "__main__":
    inicializar_db()
    app.run(host="127.0.0.1", port=5001, debug=True)


