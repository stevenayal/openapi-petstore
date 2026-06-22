# MascotasAPI — PetStore Paraguay 🇵🇾

**¡Ndaje!** El mejor PetStore del mundo, ahora desde Asunción del Paraguay.

API RESTful implementada con **Python + FastAPI** basada en la especificación OpenAPI PetStore.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
# Clonar el repositorio
git clone <repo-url>
cd openapi-petstore-py

# (Opcional) Crear y activar un entorno virtual
python -m venv venv
.\venv\Scripts\Activate    # Windows
source venv/bin/activate   # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

La API arranca en `http://localhost:8000`.

## Documentación interactiva

| Herramienta | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |

## Endpoints

### Pet (`/pet`)

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| PUT | `/pet` | Actualizar mascota | api_key |
| POST | `/pet` | Agregar mascota | api_key |
| GET | `/pet/findByStatus` | Buscar por status | api_key |
| GET | `/pet/findByTags` | Buscar por tags (deprecated) | api_key |
| GET | `/pet/{petId}` | Obtener mascota por ID | api_key |
| POST | `/pet/{petId}` | Actualizar con formulario | api_key |
| DELETE | `/pet/{petId}` | Eliminar mascota | api_key |
| POST | `/pet/{petId}/uploadImage` | Subir imagen | api_key |

### Store (`/store`)

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| GET | `/store/inventory` | Inventario por status | api_key |
| POST | `/store/order` | Crear orden | — |
| GET | `/store/order/{orderId}` | Obtener orden | — |
| DELETE | `/store/order/{orderId}` | Eliminar orden | — |

### User (`/user`)

| Método | Ruta | Descripción | Auth |
|---|---|---|---|
| POST | `/user` | Crear usuario | — |
| POST | `/user/createWithArray` | Crear usuarios (array) | — |
| POST | `/user/createWithList` | Crear usuarios (list) | — |
| GET | `/user/login` | Iniciar sesión | — |
| GET | `/user/logout` | Cerrar sesión | — |
| GET | `/user/{username}` | Obtener usuario | — |
| PUT | `/user/{username}` | Actualizar usuario | — |
| DELETE | `/user/{username}` | Eliminar usuario | — |

## Autenticación

Los endpoints de **Pet** y **Store/inventory** requieren la API Key en el header:

```
api_key: special-key
```

## Datos de ejemplo

La base se popula automáticamente al iniciar con:

- **12 mascotas** con nombres paraguayos (Tobái, Sapukái, Jagua, Mbopi, etc.)
- **10 órdenes** con comidas típicas (Sopa paraguaya, Chipa guazú, Mbeju, etc.)
- **5 usuarios** con nombres paraguayos (Juan Pérez, María González, etc.)

## Base de datos

SQLite con SQLAlchemy. El archivo `petstore.db` se crea automáticamente al iniciar.

## Toque paraguayo 🇵🇾

| Detalle | Descripción |
|---|---|
| Mascotas | Nombres en guaraní: Tobái, Sapukái, Jagua, Mbopi... |
| Categorías | Perro, Gato, Caballo, Vaca, Gallina, Cerdo... |
| Comidas | Sopa paraguaya, Chipa, Mbeju, Pastel mandi'o... |
| Usuarios | Juan Pérez, María González, Carlos Benítez... |
| Eslogan | "¡Ndaje!" — el clásico paraguayo para contar historias |

## Licencia

Apache 2.0
