"""
Script completo para configurar la base de datos desde cero.
Este script:
1. Crea la base de datos si no existe (como en MySQL)
2. Crea las tablas
3. Inserta datos de ejemplo

Ejecutar: python -m scripts.setup_db
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar ambos scripts
from scripts.create_db import create_database
from scripts.init_db import init_db


def setup_complete_database():
    """Setup completo de la base de datos."""
    print("\n")
    print("=" * 60)
    print(" " * 10 + "CONFIGURACION COMPLETA DE BASE DE DATOS")
    print("=" * 60)
    print()

    # Paso 1: Crear la base de datos
    print("PASO 1: Crear base de datos")
    print("-" * 60)
    if not create_database():
        print("\nX Error al crear la base de datos. Abortando...")
        return False

    # Paso 2: Crear tablas e insertar datos
    print("\n\nPASO 2: Crear tablas e insertar datos de ejemplo")
    print("-" * 60)
    init_db()

    print("\n")
    print("=" * 60)
    print(" " * 20 + "SETUP COMPLETADO!")
    print("=" * 60)
    print("\nTu base de datos esta lista para usar.")
    print("\nCredenciales por defecto:")
    print("  Usuario: admin")
    print("  Contrasena: admin123")
    print("\nInicia el servidor con:")
    print("  uvicorn app.main:app --reload")
    print()

    return True


if __name__ == "__main__":
    success = setup_complete_database()
    sys.exit(0 if success else 1)
