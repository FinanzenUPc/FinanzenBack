#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar la configuración de Azure
"""
import os
import sys

# Fix encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print("=" * 60)
print("DIAGNÓSTICO DE CONFIGURACIÓN PARA AZURE")
print("=" * 60)

# 1. Verificar variables de entorno
print("\n1. VARIABLES DE ENTORNO:")
print("-" * 60)

env_vars = [
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_SSLMODE",
    "SECRET_KEY",
    "DEBUG",
    "API_V1_STR",
    "PROJECT_NAME",
]

missing_vars = []
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Ocultar passwords
        if "PASSWORD" in var or "SECRET" in var:
            print(f"✓ {var}: ***{value[-4:]}")
        else:
            print(f"✓ {var}: {value}")
    else:
        print(f"✗ {var}: NO CONFIGURADA")
        if var in ["POSTGRES_HOST", "SECRET_KEY"]:
            missing_vars.append(var)

# 2. Intentar cargar la configuración
print("\n2. CARGANDO CONFIGURACIÓN:")
print("-" * 60)

try:
    from app.core.config import settings
    print("✓ Configuración cargada exitosamente")
    print(f"  - PROJECT_NAME: {settings.PROJECT_NAME}")
    print(f"  - DEBUG: {settings.DEBUG}")
    print(f"  - API_V1_STR: {settings.API_V1_STR}")

    # Mostrar DATABASE_URL (ocultando password)
    db_url = settings.DATABASE_URL
    if "postgresql" in db_url:
        # Ocultar password en la URL
        import re
        masked_url = re.sub(r'://([^:]+):([^@]+)@', r'://\1:***@', db_url)
        print(f"  - DATABASE_URL: {masked_url}")
    else:
        print(f"  - DATABASE_URL: {db_url}")

except Exception as e:
    print(f"✗ Error al cargar configuración: {e}")
    sys.exit(1)

# 3. Verificar conexión a PostgreSQL
print("\n3. CONEXIÓN A POSTGRESQL:")
print("-" * 60)

try:
    from app.core.database import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"✓ Conexión exitosa a PostgreSQL")
        print(f"  Versión: {version}")

except Exception as e:
    print(f"✗ Error de conexión: {e}")
    print("\nPosibles causas:")
    print("  - Credenciales incorrectas")
    print("  - Firewall bloqueando la conexión")
    print("  - Servidor PostgreSQL no disponible")
    print("  - SSL/TLS configuración incorrecta")

# 4. Verificar importación de módulos
print("\n4. IMPORTACIÓN DE MÓDULOS:")
print("-" * 60)

modules_to_check = [
    "fastapi",
    "uvicorn",
    "gunicorn",
    "sqlalchemy",
    "psycopg2",
    "pydantic",
    "networkx",
]

for module in modules_to_check:
    try:
        __import__(module)
        print(f"✓ {module}")
    except ImportError as e:
        print(f"✗ {module}: {e}")

# 5. Intentar importar la app
print("\n5. IMPORTACIÓN DE LA APLICACIÓN:")
print("-" * 60)

try:
    from app.main import app
    print("✓ Aplicación FastAPI importada exitosamente")
    print(f"  - Título: {app.title}")
    print(f"  - Versión: {app.version}")
    print(f"  - Docs URL: {app.docs_url}")
except Exception as e:
    print(f"✗ Error al importar app: {e}")
    import traceback
    traceback.print_exc()

# 6. Verificar tablas de la base de datos
print("\n6. VERIFICACIÓN DE TABLAS:")
print("-" * 60)

try:
    from app.core.database import engine
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if tables:
        print(f"✓ Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table}")
    else:
        print("⚠ No se encontraron tablas")
        print("  Ejecuta: python -m scripts.setup_db")

except Exception as e:
    print(f"✗ Error al verificar tablas: {e}")

# Resumen
print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)

if missing_vars:
    print(f"⚠ Variables CRÍTICAS faltantes: {', '.join(missing_vars)}")
    print("\nConfigura estas variables en Azure:")
    print("  Azure Portal > App Service > Configuration > Application settings")
else:
    print("✓ Todas las variables críticas están configuradas")

print("\nSi todo está OK, la app debería funcionar con:")
print("  gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app")
print("=" * 60)
