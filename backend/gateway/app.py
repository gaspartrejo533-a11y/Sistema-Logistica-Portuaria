

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps
import requests
import os

app = Flask(__name__)
CORS(app)

# Direcciones de los microservicios
AUTH_URL = "http://127.0.0.1:5001"
CATALOG_URL = "http://127.0.0.1:5002"
OPERATIONS_URL = "http://127.0.0.1:5003"

# Debe coincidir con la clave configurada en Auth
SECRET_KEY = os.environ["AUTH_SECRET_KEY"]

serializer = URLSafeTimedSerializer(SECRET_KEY)


# Validar el token recibido
def requiere_autenticacion(roles=None):
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            encabezado = request.headers.get("Authorization", "")

            if not encabezado.startswith("Bearer "):
                return jsonify({"error": "Token requerido"}), 401

            token = encabezado.split(" ", 1)[1]

            try:
                usuario = serializer.loads(token, max_age=3600)
            except SignatureExpired:
                return jsonify({"error": "La sesiÃ³n ha expirado"}), 401
            except BadSignature:
                return jsonify({"error": "Token invÃ¡lido"}), 401

            if roles and usuario.get("rol") not in roles:
                return jsonify({"error": "No tienes permisos"}), 403

            g.usuario = usuario
            return funcion(*args, **kwargs)

        return envoltura
    return decorador


# Verificar funcionamiento del Gateway
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "servicio": "API Gateway",
        "estado": "activo"
    }), 200


# Iniciar sesiÃ³n
@app.route("/api/login", methods=["POST"])
def login():
    try:
        respuesta = requests.post(
            f"{AUTH_URL}/login",
            json=request.get_json(silent=True),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Auth no estÃ¡ disponible"}), 503


# Registrar usuarios
@app.route("/api/usuarios", methods=["POST"])
def registrar_usuario():
    try:
        respuesta = requests.post(
            f"{AUTH_URL}/usuarios",
            json=request.get_json(silent=True),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Auth no estÃ¡ disponible"}), 503


# Consultar usuarios: solamente administrador
@app.route("/api/usuarios", methods=["GET"])
@requiere_autenticacion(["admin"])
def obtener_usuarios():
    try:
        respuesta = requests.get(
            f"{AUTH_URL}/usuarios",
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Auth no estÃ¡ disponible"}), 503


# Consultar inventario: usuarios autenticados
@app.route("/api/inventario", methods=["GET"])
@requiere_autenticacion()
def obtener_inventario():
    try:
        respuesta = requests.get(
            f"{CATALOG_URL}/inventario",
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Catalog no estÃ¡ disponible"}), 503


# Agregar recursos: solamente administrador
@app.route("/api/inventario", methods=["POST"])
@requiere_autenticacion(["admin"])
def agregar_recurso():
    try:
        respuesta = requests.post(
            f"{CATALOG_URL}/inventario",
            json=request.get_json(silent=True),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Catalog no estÃ¡ disponible"}), 503


# Consultar operaciones: usuarios autenticados
@app.route("/api/operaciones", methods=["GET"])
@requiere_autenticacion()
def obtener_operaciones():
    try:
        respuesta = requests.get(
            f"{OPERATIONS_URL}/operaciones",
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Operations no estÃ¡ disponible"}), 503


# Registrar operaciones: administrador o agente aduanal
@app.route("/api/operaciones", methods=["POST"])
@requiere_autenticacion(["admin", "agente_aduanal"])
def registrar_operacion():
    try:
        respuesta = requests.post(
            f"{OPERATIONS_URL}/operaciones",
            json=request.get_json(silent=True),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El servicio Operations no estÃ¡ disponible"}), 503

# Registrar liberaciones aduaneras
@app.route("/api/liberaciones", methods=["POST"])
@requiere_autenticacion(["admin", "agente_aduanal"])
def registrar_liberacion():
    try:
        respuesta = requests.post(
            f"{OPERATIONS_URL}/liberaciones",
            json=request.get_json(silent=True),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({
            "error": "El servicio Operations no estÃ¡ disponible"
        }), 503


# Consultar liberaciones aduaneras
@app.route("/api/liberaciones", methods=["GET"])
@requiere_autenticacion()
def obtener_liberaciones():
    try:
        respuesta = requests.get(
            f"{OPERATIONS_URL}/liberaciones",
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({
            "error": "El servicio Operations no estÃ¡ disponible"
        }), 503


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

