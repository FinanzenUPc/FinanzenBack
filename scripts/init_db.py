"""
Script para inicializar la base de datos con datos de ejemplo.
Ejecutar: python -m scripts.init_db
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.transaction import Transaction
from app.core.security import get_password_hash


def init_db():
    """Initialize database with sample data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                email="admin@finanzen.com",
                username="admin",
                full_name="Administrator",
                hashed_password=get_password_hash("admin123"),
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"Admin user created with ID: {admin.id}")

            # Create sample transactions
            print("Creating sample transactions...")
            from datetime import date
            sample_transactions = [
                Transaction(
                    fecha=date.today(),
                    tipo="ingreso",
                    categoria="Salario",
                    descripcion="Salario mensual",
                    metodo_pago="Transferencia",
                    monto=1000.0,
                    usuario=admin.username
                ),
                Transaction(
                    fecha=date.today(),
                    tipo="egreso",
                    categoria="Comida",
                    descripcion="Supermercado",
                    metodo_pago="Tarjeta",
                    monto=50.0,
                    usuario=admin.username
                ),
                Transaction(
                    fecha=date.today(),
                    tipo="egreso",
                    categoria="Transporte",
                    descripcion="Gasolina",
                    metodo_pago="Efectivo",
                    monto=100.0,
                    usuario=admin.username
                ),
            ]

            for trans in sample_transactions:
                db.add(trans)

            db.commit()
            print(f"Created {len(sample_transactions)} sample transactions")
        else:
            print("Admin user already exists. Skipping initialization.")

        print("\nDatabase initialization completed!")
        print("\nDefault credentials:")
        print("Username: admin")
        print("Password: admin123")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
