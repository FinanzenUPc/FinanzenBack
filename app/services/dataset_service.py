"""
Dataset Service - Manejo de carga y normalización de datasets
"""
import pandas as pd
import io
from typing import Dict, List, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.transaction import Transaction


class DatasetService:
    """Servicio para manejo de datasets de transacciones."""

    @staticmethod
    def parse_csv(file_content: bytes) -> pd.DataFrame:
        """
        Parsea archivo CSV a DataFrame.
        Intenta con diferentes separadores y encodings.

        Args:
            file_content: Contenido del archivo CSV

        Returns:
            DataFrame con los datos
        """
        # Intentar diferentes configuraciones
        configs = [
            {'sep': ',', 'encoding': 'utf-8'},
            {'sep': ';', 'encoding': 'utf-8'},
            {'sep': ',', 'encoding': 'latin-1'},
            {'sep': ';', 'encoding': 'latin-1'},
            {'sep': ',', 'encoding': 'iso-8859-1'},
            {'sep': ';', 'encoding': 'iso-8859-1'},
        ]

        last_error = None
        for config in configs:
            try:
                df = pd.read_csv(io.BytesIO(file_content), **config)
                # Normalizar nombres de columnas (quitar espacios, convertir a minúsculas)
                df.columns = df.columns.str.strip().str.lower()
                # Si tiene al menos 2 columnas, probablemente sea válido
                if len(df.columns) >= 2:
                    return df
            except Exception as e:
                last_error = e
                continue

        # Si ninguna configuración funcionó, lanzar el último error
        if last_error:
            raise last_error

        # Intento por defecto
        df = pd.read_csv(io.BytesIO(file_content))
        df.columns = df.columns.str.strip().str.lower()
        return df

    @staticmethod
    def validate_schema(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Valida el esquema del dataset.

        Args:
            df: DataFrame a validar

        Returns:
            Dict con resultado de validación
        """
        required_columns = ['fecha', 'tipo', 'categoria', 'monto', 'usuario']
        optional_columns = ['subcategoria', 'descripcion', 'metodo_pago']

        missing_columns = [col for col in required_columns if col not in df.columns]
        present_columns = list(df.columns)

        return {
            "is_valid": len(missing_columns) == 0,
            "missing_columns": missing_columns,
            "present_columns": present_columns,
            "num_rows": len(df),
            "schema": {col: str(df[col].dtype) for col in df.columns}
        }

    @staticmethod
    def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza los datos del dataset.

        Args:
            df: DataFrame original

        Returns:
            DataFrame normalizado
        """
        df_normalized = df.copy()

        # Convertir fecha a formato estándar
        if 'fecha' in df_normalized.columns:
            df_normalized['fecha'] = pd.to_datetime(df_normalized['fecha'], errors='coerce')

        # Normalizar tipo (ingreso/egreso) - manejar NaN
        if 'tipo' in df_normalized.columns:
            # Convertir a string primero para evitar errores con NaN
            df_normalized['tipo'] = df_normalized['tipo'].astype(str).str.lower().str.strip()
            # Reemplazar 'nan' string con NaN real
            df_normalized['tipo'] = df_normalized['tipo'].replace('nan', pd.NA)

        # Normalizar categoría - manejar NaN
        if 'categoria' in df_normalized.columns:
            df_normalized['categoria'] = df_normalized['categoria'].astype(str).str.strip()
            df_normalized['categoria'] = df_normalized['categoria'].replace('nan', pd.NA)

        # Normalizar subcategoría si existe
        if 'subcategoria' in df_normalized.columns:
            df_normalized['subcategoria'] = df_normalized['subcategoria'].astype(str).str.strip()
            df_normalized['subcategoria'] = df_normalized['subcategoria'].replace('nan', pd.NA)

        # Normalizar descripción si existe
        if 'descripcion' in df_normalized.columns:
            df_normalized['descripcion'] = df_normalized['descripcion'].astype(str).str.strip()
            df_normalized['descripcion'] = df_normalized['descripcion'].replace('nan', pd.NA)

        # Normalizar método de pago si existe
        if 'metodo_pago' in df_normalized.columns:
            df_normalized['metodo_pago'] = df_normalized['metodo_pago'].astype(str).str.strip()
            df_normalized['metodo_pago'] = df_normalized['metodo_pago'].replace('nan', pd.NA)

        # Normalizar usuario
        if 'usuario' in df_normalized.columns:
            df_normalized['usuario'] = df_normalized['usuario'].astype(str).str.strip()
            df_normalized['usuario'] = df_normalized['usuario'].replace('nan', pd.NA)

        # Convertir monto a float
        if 'monto' in df_normalized.columns:
            df_normalized['monto'] = pd.to_numeric(df_normalized['monto'], errors='coerce')

        # Eliminar filas con datos nulos críticos
        df_normalized = df_normalized.dropna(subset=['fecha', 'tipo', 'categoria', 'monto', 'usuario'])

        return df_normalized

    @staticmethod
    def save_to_db(df: pd.DataFrame, db: Session) -> Dict[str, Any]:
        """
        Guarda DataFrame en la base de datos.

        Args:
            df: DataFrame normalizado
            db: Sesión de base de datos

        Returns:
            Dict con resultado de la operación
        """
        created_count = 0
        errors = []

        for idx, row in df.iterrows():
            try:
                transaction = Transaction(
                    fecha=row['fecha'],
                    tipo=row['tipo'],
                    categoria=row['categoria'],
                    subcategoria=row.get('subcategoria'),
                    descripcion=row.get('descripcion'),
                    metodo_pago=row.get('metodo_pago'),
                    monto=row['monto'],
                    usuario=row['usuario']
                )
                db.add(transaction)
                created_count += 1
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")

        db.commit()

        return {
            "created_count": created_count,
            "errors": errors,
            "success": len(errors) == 0
        }

    @staticmethod
    def get_dataset_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtiene estadísticas del dataset.

        Args:
            df: DataFrame

        Returns:
            Dict con estadísticas
        """
        stats = {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "columns": list(df.columns),
        }

        # Estadísticas de monto - manejar DataFrame vacío o valores NaN
        if 'monto' in df.columns and len(df) > 0:
            monto_valid = df['monto'].dropna()
            if len(monto_valid) > 0:
                stats["monto_stats"] = {
                    "mean": float(monto_valid.mean()) if not pd.isna(monto_valid.mean()) else 0.0,
                    "median": float(monto_valid.median()) if not pd.isna(monto_valid.median()) else 0.0,
                    "std": float(monto_valid.std()) if not pd.isna(monto_valid.std()) else 0.0,
                    "min": float(monto_valid.min()) if not pd.isna(monto_valid.min()) else 0.0,
                    "max": float(monto_valid.max()) if not pd.isna(monto_valid.max()) else 0.0,
                    "sum": float(monto_valid.sum()) if not pd.isna(monto_valid.sum()) else 0.0
                }
            else:
                stats["monto_stats"] = {
                    "mean": 0.0, "median": 0.0, "std": 0.0,
                    "min": 0.0, "max": 0.0, "sum": 0.0
                }

        # Distribución de tipo
        if 'tipo' in df.columns and len(df) > 0:
            tipo_counts = df['tipo'].value_counts()
            stats["tipo_distribution"] = {str(k): int(v) for k, v in tipo_counts.items()}

        # Distribución de categoría (top 10)
        if 'categoria' in df.columns and len(df) > 0:
            categoria_counts = df['categoria'].value_counts().head(10)
            stats["categoria_distribution"] = {str(k): int(v) for k, v in categoria_counts.items()}

        # Número de usuarios únicos
        if 'usuario' in df.columns and len(df) > 0:
            stats["num_users"] = int(df['usuario'].nunique())

        return stats


dataset_service = DatasetService()
