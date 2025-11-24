"""
Script para crear la base de datos PostgreSQL automáticamente.
Similar a cómo funciona en MySQL.

Ejecutar: python -m scripts.create_db
"""
import sys
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()


def create_database():
    """Crea la base de datos si no existe."""

    # Leer configuración del .env
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "1234")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5434")
    db_name = os.getenv("POSTGRES_DB", "finanzen_db")

    print("=" * 60)
    print("CREACIÓN DE BASE DE DATOS POSTGRESQL")
    print("=" * 60)
    print(f"Host: {db_host}:{db_port}")
    print(f"Usuario: {db_user}")
    print(f"Base de datos: {db_name}")
    print("=" * 60)

    try:
        # Conectarse a la base de datos 'postgres' por defecto
        print("\n[1/3] Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print("OK Conexion exitosa a PostgreSQL")

        # Verificar si la base de datos existe
        print(f"\n[2/3] Verificando si la base de datos '{db_name}' existe...")
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()

        if exists:
            print(f"OK La base de datos '{db_name}' ya existe")
        else:
            # Crear la base de datos
            print(f"X La base de datos '{db_name}' no existe")
            print(f"\n[3/3] Creando base de datos '{db_name}'...")
            cursor.execute(f'CREATE DATABASE {db_name}')
            print(f"OK Base de datos '{db_name}' creada exitosamente!")

        cursor.close()
        conn.close()

        print("\n" + "=" * 60)
        print("PROCESO COMPLETADO")
        print("=" * 60)
        print(f"Base de datos: {db_name}")
        print(f"URL de conexión: postgresql://{db_user}:****@{db_host}:{db_port}/{db_name}")
        print("\nAhora puedes ejecutar:")
        print("  python -m scripts.init_db    (para crear tablas e insertar datos)")
        print("  uvicorn app.main:app --reload (para iniciar el servidor)")
        print("=" * 60)

        return True

    except psycopg2.OperationalError as e:
        print("\nX ERROR DE CONEXION")
        print("-" * 60)
        print("No se pudo conectar a PostgreSQL.")
        print("\nVerifica que:")
        print(f"  1. PostgreSQL este corriendo en {db_host}:{db_port}")
        print(f"  2. El usuario '{db_user}' existe")
        print(f"  3. La contrasena sea correcta")
        print(f"\nError: {e}")
        print("-" * 60)
        return False

    except Exception as e:
        print(f"\nX ERROR: {e}")
        return False


if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)
