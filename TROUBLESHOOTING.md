# Solución de Problemas: Application Error en Azure

## Problema: Application Error en Azure Web App

Si ves "Application Error" en https://finanzenbackend-fednf3ejg0hheqaq.canadacentral-01.azurewebsites.net/, sigue estos pasos:

---

## ✅ CHECKLIST DE VERIFICACIÓN

### 1. Variables de Entorno en Azure App Service

Ve a: **Azure Portal > App Service > finanzenbackend > Configuration > Application settings**

Verifica que tengas EXACTAMENTE estas variables:

```
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_HOST=tu-servidor.postgres.database.azure.com
POSTGRES_PORT=5432
POSTGRES_DB=finanzen_db
POSTGRES_SSLMODE=require
SECRET_KEY=una-clave-secreta-larga-y-segura
DEBUG=False
```

**IMPORTANTE:**
- ✅ POSTGRES_SSLMODE debe ser `require` (no `disable`)
- ✅ POSTGRES_HOST debe terminar en `.postgres.database.azure.com`
- ✅ SECRET_KEY debe ser una cadena larga y aleatoria
- ✅ DEBUG debe ser `False` en producción

Después de agregar/modificar variables:
1. Click en "Save" (arriba)
2. Click en "Continue" para confirmar
3. Espera a que se guarden los cambios

---

### 2. Firewall de PostgreSQL

**MUY IMPORTANTE:** Azure App Service necesita acceso a tu base de datos PostgreSQL.

Ve a: **Azure Portal > Azure Database for PostgreSQL > tu-servidor > Networking**

#### Opción A: Permitir servicios de Azure (Recomendado)
- ✅ Marca la casilla: **"Allow public access from any Azure service within Azure to this server"**
- Click en "Save"

#### Opción B: Agregar reglas de firewall específicas
Si la opción A no funciona, agrega las IPs de salida de tu App Service:

1. Ve a: **App Service > finanzenbackend > Properties**
2. Copia todas las "Outbound IP Addresses"
3. Ve a: **PostgreSQL > Networking > Firewall rules**
4. Agrega cada IP como una regla nueva
5. Click en "Save"

---

### 3. Usuario de PostgreSQL

**IMPORTANTE:** Azure PostgreSQL usa un formato especial para el usuario.

El usuario debe ser: `usuario@nombre-servidor`

**Ejemplo:**
- Si tu servidor es: `finanzen-db.postgres.database.azure.com`
- Y tu usuario es: `adminuser`
- Entonces POSTGRES_USER debe ser: `adminuser@finanzen-db`

**Verifica en Azure Portal > Configuration > Application settings:**
```
POSTGRES_USER=adminuser@finanzen-db
```

---

### 4. Startup Command

Ve a: **Azure Portal > App Service > Configuration > General settings**

En "Startup Command" debe estar:
```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:${PORT:-8000}
```

O simplemente:
```
bash startup.sh
```

Click en "Save"

---

### 5. Verificar que la Base de Datos existe

Conéctate a tu PostgreSQL usando:
- Azure Cloud Shell
- pgAdmin
- Azure Data Studio

Y verifica que:
1. La base de datos `finanzen_db` existe
2. El usuario tiene permisos para acceder a ella

SQL para crear la base de datos si no existe:
```sql
CREATE DATABASE finanzen_db;
```

---

### 6. Reiniciar el App Service

Después de hacer cambios:

1. Ve a: **Azure Portal > App Service > finanzenbackend**
2. Click en "Restart" (arriba)
3. Espera 2-3 minutos

---

### 7. Ver los Logs en Tiempo Real

Para ver qué está pasando:

#### Opción A: Portal de Azure
1. Ve a: **Azure Portal > App Service > finanzenbackend > Log stream**
2. Espera a que se conecte
3. Reinicia el servicio y observa los logs

#### Opción B: Azure CLI (si tienes instalado)
```bash
az webapp log tail --name finanzenbackend --resource-group DefaultResourceGroup-CC
```

---

### 8. Habilitar Logging Detallado

Ve a: **Azure Portal > App Service > App Service logs**

Configura:
- **Application Logging**: On
- **Level**: Verbose
- **Web server logging**: File System
- Click en "Save"

Ahora ve a "Log stream" para ver logs detallados.

---

## 🔍 ERRORES COMUNES Y SOLUCIONES

### Error: "could not connect to server"
**Causa:** Firewall de PostgreSQL bloqueando la conexión

**Solución:**
1. Ve a PostgreSQL > Networking
2. Habilita "Allow public access from any Azure service"
3. Reinicia App Service

---

### Error: "FATAL: no pg_hba.conf entry for host"
**Causa:** IP de App Service no está en firewall de PostgreSQL

**Solución:**
1. Obtén las IPs de salida del App Service (Properties > Outbound IP Addresses)
2. Agrégalas al firewall de PostgreSQL
3. Reinicia App Service

---

### Error: "password authentication failed"
**Causa:** Usuario o contraseña incorrectos, o formato de usuario incorrecto

**Solución:**
1. Verifica que POSTGRES_USER sea: `usuario@nombre-servidor`
2. Verifica que POSTGRES_PASSWORD sea correcta
3. Prueba conectarte manualmente a PostgreSQL con esas credenciales

---

### Error: "SSL connection is required"
**Causa:** PostgreSQL requiere SSL pero POSTGRES_SSLMODE está mal configurado

**Solución:**
1. Asegúrate que POSTGRES_SSLMODE=require (no "disable")
2. Reinicia App Service

---

### Error: "Module not found" o "Import Error"
**Causa:** Dependencias no instaladas correctamente

**Solución:**
1. Verifica que requirements.txt esté completo
2. Verifica que el deployment se completó exitosamente
3. Ve a "Deployment Center" y revisa el último deployment

---

## 🧪 PRUEBA DE DIAGNÓSTICO

He creado un script `test_azure_config.py` que puedes usar para probar.

Para ejecutarlo localmente:
```bash
python test_azure_config.py
```

Esto te mostrará si hay problemas con la configuración.

---

## ✅ VERIFICACIÓN FINAL

Una vez que hayas verificado todo:

1. **Reinicia el App Service**
2. **Espera 2-3 minutos**
3. **Prueba estos endpoints:**
   - https://finanzenbackend-fednf3ejg0hheqaq.canadacentral-01.azurewebsites.net/health
   - https://finanzenbackend-fednf3ejg0hheqaq.canadacentral-01.azurewebsites.net/
   - https://finanzenbackend-fednf3ejg0hheqaq.canadacentral-01.azurewebsites.net/api/v1/docs

Si ves `{"status":"healthy"}` en /health, ¡la app está funcionando! 🎉

---

## 📞 SIGUIENTE PASO SI SIGUE FALLANDO

Si después de todo esto sigue fallando:

1. Ve a **Log stream**
2. Copia el error completo que aparece
3. Compártelo para poder ayudarte mejor

Los errores más útiles empiezan con:
- `ERROR`
- `CRITICAL`
- `Traceback`
- `Exception`
