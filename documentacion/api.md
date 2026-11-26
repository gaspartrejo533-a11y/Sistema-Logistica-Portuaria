
# Documentación de API REST
## Sistema de Gestión de Logística Portuaria

## 1. API Gateway

Dirección base: `http://127.0.0.1:5000`

El API Gateway es el punto de entrada del frontend y distribuye las solicitudes a los microservicios.

| Método | Endpoint | Descripción | Acceso |
|---|---|---|---|
| GET | /health | Verificar Gateway | Público |
| POST | /api/login | Iniciar sesión | Público |
| POST | /api/usuarios | Registrar usuario | Público, roles no administrativos |
| GET | /api/usuarios | Consultar usuarios | Administrador |
| GET | /api/inventario | Consultar inventario | Autenticado |
| POST | /api/inventario | Registrar inventario | Administrador |
| GET | /api/operaciones | Consultar operaciones | Autenticado |
| POST | /api/operaciones | Registrar operación | Administrador y agente aduanal |
| GET | /api/liberaciones | Consultar liberaciones | Autenticado |
| POST | /api/liberaciones | Registrar liberación | Administrador y agente aduanal |

## 2. Microservicio Auth

Dirección base: `http://127.0.0.1:5001`

Responsable de administrar usuarios y autenticación.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /health | Estado del servicio |
| POST | /login | Validar credenciales y generar token |
| POST | /usuarios | Registrar usuario |
| GET | /usuarios | Consultar usuarios |

Base de datos: `auth.db`

## 3. Microservicio Catalog

Dirección base: `http://127.0.0.1:5002`

Responsable del inventario portuario.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /health | Estado del servicio |
| GET | /inventario | Consultar inventario |
| POST | /inventario | Registrar recurso, si está habilitado en la implementación |

Base de datos: `catalog.db`

## 4. Microservicio Operations

Dirección base: `http://127.0.0.1:5003`

Responsable de las operaciones portuarias y liberaciones aduaneras.

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /health | Estado del servicio |
| GET | /operaciones | Consultar operaciones |
| POST | /operaciones | Registrar operación |
| GET | /liberaciones | Consultar liberaciones |
| POST | /liberaciones | Registrar liberación |

Base de datos: `operations.db`

## 5. Autenticación

Las rutas protegidas del Gateway reciben un token mediante el encabezado HTTP:

`Authorization: Bearer TOKEN`

El token se obtiene al iniciar sesión mediante POST `/api/login`.

## 6. Ejemplo de inicio de sesión

Solicitud:

Método: POST

Endpoint: `/api/login`

Ejemplo de cuerpo JSON:

```json
{
  "correo": "usuario@puerto.com",
  "password": "********"
}
```

Respuesta esperada:

```json
{
  "mensaje": "Inicio de sesión exitoso",
  "token": "TOKEN_GENERADO",
  "usuario": {
    "id": 1,
    "nombre": "Usuario de prueba",
    "correo": "usuario@puerto.com",
    "rol": "operador"
  }
}
```

## 7. Códigos de respuesta HTTP

| Código | Significado |
|---|---|
| 200 | Solicitud exitosa |
| 201 | Registro creado |
| 400 | Datos incorrectos o incompletos |
| 401 | No autenticado |
| 403 | Sin permisos |
| 404 | Recurso no encontrado |
| 409 | Conflicto, por ejemplo correo duplicado |
| 500 | Error interno del servicio |
| 503 | Servicio no disponible |

## 8. Observaciones

Las rutas documentadas corresponden a la estructura implementada y probada durante el desarrollo. Las funcionalidades adicionales deberán documentarse cuando se incorporen.
