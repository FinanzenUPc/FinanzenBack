# Configuración de Azure Web App

## Variables de Entorno Requeridas

Para que la aplicación funcione en Azure, necesitas configurar las siguientes variables de entorno en el portal de Azure:

### Ir a: Azure Portal > App Service > finanzenbackend > Configuration > Application settings

Agrega las siguientes variables:

### 1. PostgreSQL Database (OBLIGATORIO)
```
POSTGRES_USER=<tu_usuario_postgres>
POSTGRES_PASSWORD=<tu_password_postgres>
POSTGRES_HOST=<tu_servidor_postgres>.postgres.database.azure.com
POSTGRES_PORT=5432
POSTGRES_DB=finanzen_db
POSTGRES_SSLMODE=require
```

### 2. Security (OBLIGATORIO)
```
SECRET_KEY=<genera_una_clave_secreta_fuerte>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. API Configuration
```
API_V1_STR=/api/v1
PROJECT_NAME=Finanzen Backend
DEBUG=False
```

### 4. CORS Origins
```
BACKEND_CORS_ORIGINS=["https://tu-frontend.com","http://localhost:3000"]
```

## Comando de Inicio (Startup Command)

En Azure Portal > App Service > Configuration > General settings > Startup Command:

```
bash startup.sh
```

O alternativamente:
```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT:-8000}
```

## Base de Datos PostgreSQL en Azure

Si no tienes una base de datos PostgreSQL en Azure, créala:

1. Ve a Azure Portal > Create a resource > Azure Database for PostgreSQL
2. Selecciona "Flexible Server"
3. Configura:
   - Server name: finanzen-db
   - Region: Canada Central (mismo que tu app)
   - PostgreSQL version: 15 o superior
   - Compute + storage: Selecciona según necesidad
4. En "Networking":
   - Marca "Allow public access from any Azure service"
   - Agrega tu IP para administración
5. Crea el servidor

Después de crear el servidor:
- Anota el hostname (ej: finanzen-db.postgres.database.azure.com)
- Anota el usuario y password
- Crea la base de datos "finanzen_db" usando pgAdmin o Azure Portal

## Firewall Rules

Asegúrate de que tu Azure PostgreSQL permite conexiones desde tu App Service:

1. Ve a PostgreSQL server > Networking
2. Agrega una regla de firewall para permitir Azure services
3. O agrega la IP de salida de tu App Service

## Verificar Deployment

Después de configurar todo:

1. Guarda los cambios en Configuration
2. Reinicia el App Service
3. Ve a: https://finanzenbackend-fednf3ejg0hheqaq.canadacentral-01.azurewebsites.net/health
4. Deberías ver: `{"status":"healthy"}`

## Ver Logs

Para ver logs en tiempo real:

```bash
az webapp log tail --name finanzenbackend --resource-group DefaultResourceGroup-CC
```

O en el portal:
Azure Portal > App Service > finanzenbackend > Log stream

## Troubleshooting

### Error: Application Error

Posibles causas:
1. Faltan variables de entorno
2. No se puede conectar a PostgreSQL
3. Startup command incorrecto

Solución:
- Verifica todas las variables de entorno
- Verifica que PostgreSQL esté accesible
- Revisa los logs en Log stream

### Error: Can't connect to database

Solución:
- Verifica POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD
- Verifica que el firewall de PostgreSQL permita la conexión
- Verifica que POSTGRES_SSLMODE esté en "require" para Azure

### La app usa SQLite en lugar de PostgreSQL

Si no configuraste las variables de PostgreSQL, la app automáticamente usa SQLite local (no recomendado para producción).

Solución: Configura todas las variables POSTGRES_* en Application settings.
