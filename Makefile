.PHONY: help install run test clean migrate setup-db create-db init-db format lint

help:
	@echo "Comandos disponibles:"
	@echo "  make install   - Instalar dependencias"
	@echo "  make run       - Ejecutar servidor de desarrollo"
	@echo "  make test      - Ejecutar tests"
	@echo "  make clean     - Limpiar archivos temporales"
	@echo "  make setup-db  - Crear DB + tablas + datos (COMPLETO)"
	@echo "  make create-db - Crear solo la base de datos"
	@echo "  make init-db   - Crear solo tablas e insertar datos"
	@echo "  make migrate   - Ejecutar migraciones de Alembic"
	@echo "  make format    - Formatear código con black e isort"
	@echo "  make lint      - Verificar código con flake8 y mypy"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest --cov=app tests/

clean:
	@echo "Limpiando archivos temporales..."
	@python scripts/clean.py || (find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; \
	find . -type f -name "*.pyc" -delete 2>/dev/null; \
	find . -type f -name "*.pyo" -delete 2>/dev/null; \
	find . -type f -name "*.coverage" -delete 2>/dev/null; \
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null; \
	echo "Limpieza completada!")

setup-db:
	python -m scripts.setup_db

create-db:
	python -m scripts.create_db

init-db:
	python -m scripts.init_db

migrate:
	alembic upgrade head

format:
	black app/ tests/
	isort app/ tests/

lint:
	flake8 app/ tests/
	mypy app/
