# Finanzen Backend API

Backend de la aplicación Finanzen desarrollado con FastAPI, PostgreSQL y algoritmos de grafos para análisis financiero.

## Características

- Framework: FastAPI
- Base de datos: PostgreSQL
- ORM: SQLAlchemy
- Migraciones: Alembic
- Autenticación: JWT (JSON Web Tokens)
- Documentación automática: OpenAPI/Swagger
- Contenedores: Docker & Docker Compose
- Algoritmos de grafos: NetworkX (Dijkstra, análisis de centralidad, detección de ciclos)

## Estructura del Proyecto

```
BACKEND/
├── app/
│   ├── algorithms/          # Algoritmos de grafos para análisis financiero
│   ├── core/                # Configuración, database, security
│   ├── models/              # Modelos SQLAlchemy
│   ├── routers/             # Endpoints de la API
│   ├── schemas/             # Schemas Pydantic
│   ├── services/            # Lógica de negocio
│   └── utils/               # Utilidades
├── alembic/                 # Migraciones de base de datos
├── tests/                   # Tests
├── scripts/                 # Scripts útiles
├── .env                     # Variables de entorno
├── docker-compose.yml       # Configuración Docker Compose
├── Dockerfile               # Configuración Docker
└── requirements.txt         # Dependencias Python
```

## Requisitos Previos

- Python 3.11+
- PostgreSQL 15+ (o usar Docker)
- Docker & Docker Compose (opcional pero recomendado)


## Uso de la API

### Endpoints Principales

#### Autenticación

- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Login y obtener token

#### Transacciones

- `GET /api/v1/transactions/` - Listar transacciones
- `POST /api/v1/transactions/` - Crear transacción
- `GET /api/v1/transactions/{id}` - Obtener transacción
- `PUT /api/v1/transactions/{id}` - Actualizar transacción
- `DELETE /api/v1/transactions/{id}` - Eliminar transacción

#### Health Check

- `GET /health` - Estado del servidor

### Documentación Interactiva

Una vez que el servidor esté corriendo, accede a:

- Swagger UI: <http://localhost:8000/api/v1/docs>
- ReDoc: <http://localhost:8000/api/v1/redoc>

## Algoritmos de Grafos

El backend incluye análisis financiero usando algoritmos de grafos:

- **Dijkstra**: Encontrar caminos óptimos entre transacciones
- **Análisis de Centralidad**: Identificar transacciones o categorías más importantes
- **Detección de Ciclos**: Detectar patrones de gasto circular
- **Análisis de Flujo**: Análisis de flujo de caja

