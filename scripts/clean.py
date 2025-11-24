"""
Script de limpieza del proyecto
Ejecutar: python scripts/clean.py
"""
import os
import shutil
from pathlib import Path


def clean_project():
    """Limpia archivos temporales y cache del proyecto."""
    root = Path(__file__).parent.parent
    cleaned = []

    # Patrones a limpiar
    patterns = {
        '__pycache__': 'directories',
        '*.pyc': 'files',
        '*.pyo': 'files',
        '*.pyd': 'files',
        '.pytest_cache': 'directories',
        '.mypy_cache': 'directories',
        '.coverage': 'files',
        'coverage.xml': 'files',
        'htmlcov': 'directories',
        '.tox': 'directories',
        '.hypothesis': 'directories',
        '*.log': 'files',
        '*.tmp': 'files',
        '.DS_Store': 'files',
    }

    print("🧹 Iniciando limpieza del proyecto...\n")

    # Limpiar directorios
    for pattern, item_type in patterns.items():
        if item_type == 'directories':
            for item in root.rglob(pattern):
                if item.is_dir() and '.venv' not in str(item):
                    try:
                        shutil.rmtree(item)
                        cleaned.append(f"📁 {item.relative_to(root)}")
                    except Exception as e:
                        print(f"❌ Error eliminando {item}: {e}")

        elif item_type == 'files':
            for item in root.rglob(pattern):
                if item.is_file() and '.venv' not in str(item):
                    try:
                        item.unlink()
                        cleaned.append(f"📄 {item.relative_to(root)}")
                    except Exception as e:
                        print(f"❌ Error eliminando {item}: {e}")

    if cleaned:
        print(f"✅ Limpiados {len(cleaned)} items:")
        for item in cleaned[:20]:  # Mostrar solo los primeros 20
            print(f"   {item}")
        if len(cleaned) > 20:
            print(f"   ... y {len(cleaned) - 20} más")
    else:
        print("✅ No hay nada que limpiar. Proyecto limpio!")

    print(f"\n🎉 Limpieza completada!")


if __name__ == "__main__":
    clean_project()
