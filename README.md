# Sistema de Gestion de Logistica Portuaria
## Proyecto Final - Arquitectura de Microservicios

### 1. Descripcion
Sistema web para apoyar la gestion de operaciones de un puerto de altura. Permite administrar usuarios, inventario, operaciones portuarias y liberaciones aduaneras.

### 2. Arquitectura
El sistema utiliza una arquitectura de microservicios. El frontend se comunica con el API Gateway, que distribuye las solicitudes a los servicios correspondientes.

### 3. Tecnologias
- Python
- Flask
- SQLite
- HTML, CSS y JavaScript
- API REST
- HTTP y JSON

### 4. Requisitos
- Windows 10 u 11.
- Python instalado.
- Python Launcher disponible mediante el comando py.
- Navegador web.
- Visual Studio Code (recomendado).

No se requiere Docker para ejecutar esta version del proyecto.

### 5. Instalacion
Abrir PowerShell en la carpeta principal del proyecto y ejecutar:

```powershell
py -m pip install -r requirements.txt
```

### 6. Ejecucion
Desde la carpeta principal ejecutar:

```powershell
.\iniciar_sistema.bat
```

El archivo inicia los cuatro procesos del sistema en ventanas independientes.

### 7. Puertos
| Componente | Puerto |
|---|---:|
| API Gateway | 5000 |
| Auth | 5001 |
| Catalog | 5002 |
| Operations | 5003 |

### 8. Frontend
Abrir el archivo frontend/index.html en el navegador. Tambien puede utilizarse la extension Live Server de Visual Studio Code.

La direccion del API Gateway es:

http://127.0.0.1:5000

### 9. Bases de datos
Cada microservicio administra su propia base de datos SQLite:

- backend/auth/auth.db
- backend/catalog/catalog.db
- backend/operations/operations.db

El API Gateway no utiliza una base de datos propia.

### 10. Documentacion de API
Consultar documentacion/api.md para revisar los endpoints, metodos HTTP, autenticacion y ejemplos de solicitudes.

### 11. Diagrama de arquitectura
Consultar documentacion/arquitectura.md.

### 12. Evidencias
Las capturas de funcionamiento se encuentran en la carpeta evidencias.

### 13. Seguridad y configuracion
Auth y Gateway deben utilizar la misma clave AUTH_SECRET_KEY para la firma y validacion de tokens.

Para configurar una clave compartida desde PowerShell antes de iniciar el sistema:

```powershell
$env:AUTH_SECRET_KEY = "CAMBIA_POR_UNA_CLAVE_SEGURA"
.\iniciar_sistema.bat
```

La clave de ejemplo incluida en el codigo es solamente para pruebas. Debe cambiarse antes de utilizar el sistema en produccion.

### 14. Integrantes
- Gaspar Trejo Martinez
- Ana Merly Caballero Canul

Carrera: Ingenieria en Sistemas Computacionales.

### 15. Conclusion
El proyecto permite aplicar los principios de arquitectura de microservicios mediante la separacion de responsabilidades, la comunicacion por API REST y el uso de bases de datos independientes. Esta organizacion facilita el mantenimiento y la ampliacion del sistema.
