"""
Dataset Router - Endpoints para manejo de datasets
"""
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.services.dataset_service import dataset_service

router = APIRouter(prefix="/dataset", tags=["Dataset"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    normalize: bool = True,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Carga un dataset CSV de transacciones.

    Args:
        file: Archivo CSV
        normalize: Si se debe normalizar los datos
        db: Sesión de base de datos

    Returns:
        Resultado de la carga
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se permiten archivos CSV"
        )

    try:
        content = await file.read()
        df = dataset_service.parse_csv(content)

        validation = dataset_service.validate_schema(df)
        if not validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Esquema inválido. Columnas faltantes: {validation['missing_columns']}"
            )

        if normalize:
            df = dataset_service.normalize_data(df)

        stats = dataset_service.get_dataset_stats(df)
        save_result = dataset_service.save_to_db(df, db)

        return {
            "message": "Dataset cargado exitosamente",
            "validation": validation,
            "statistics": stats,
            "save_result": save_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando dataset: {str(e)}"
        )


@router.get("/schema")
def get_schema() -> Dict[str, Any]:
    """
    Obtiene el esquema esperado del dataset.

    Returns:
        Esquema del dataset
    """
    return {
        "required_columns": {
            "fecha": "date (YYYY-MM-DD)",
            "tipo": "string (ingreso/egreso)",
            "categoria": "string",
            "monto": "float",
            "usuario": "string"
        },
        "optional_columns": {
            "subcategoria": "string",
            "descripcion": "string",
            "metodo_pago": "string"
        },
        "example": {
            "fecha": "2024-01-15",
            "tipo": "egreso",
            "categoria": "Comida",
            "subcategoria": "Restaurante",
            "descripcion": "Almuerzo",
            "metodo_pago": "Tarjeta",
            "monto": 25.50,
            "usuario": "user123"
        }
    }


@router.post("/normalize")
async def normalize_dataset(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Normaliza un dataset sin guardarlo.

    Args:
        file: Archivo CSV

    Returns:
        Dataset normalizado y estadísticas
    """
    # Validar tipo de archivo
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se permiten archivos CSV"
        )

    try:
        # Leer y parsear CSV
        content = await file.read()
        df = dataset_service.parse_csv(content)

        # Validar que el CSV no esté vacío
        if len(df) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo CSV está vacío"
            )

        # Validar esquema
        validation = dataset_service.validate_schema(df)
        if not validation["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Esquema inválido",
                    "columnas_requeridas": ['fecha', 'tipo', 'categoria', 'monto', 'usuario'],
                    "columnas_faltantes": validation['missing_columns'],
                    "columnas_detectadas": validation['present_columns'],
                    "sugerencia": "Verifica que los nombres de las columnas coincidan exactamente (en minúsculas)"
                }
            )

        # Normalizar datos
        df_normalized = dataset_service.normalize_data(df)

        # Calcular estadísticas
        stats_before = dataset_service.get_dataset_stats(df)
        stats_after = dataset_service.get_dataset_stats(df_normalized)

        return {
            "message": "Dataset normalizado exitosamente",
            "rows_before": len(df),
            "rows_after": len(df_normalized),
            "rows_removed": len(df) - len(df_normalized),
            "validation": validation,
            "statistics_before": stats_before,
            "statistics_after": stats_after
        }

    except HTTPException:
        raise
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo CSV está vacío o mal formado"
        )
    except pd.errors.ParserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al parsear CSV: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error normalizando dataset: {str(e)}"
        )
