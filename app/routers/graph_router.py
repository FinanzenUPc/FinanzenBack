"""
Graph Router - Endpoints para construcción y estadísticas de grafos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.services.graph_service import graph_service

router = APIRouter(prefix="/graphs", tags=["Graphs"])


# ==================== Pydantic Models ====================

class GraphBuildRequest(BaseModel):
    """Request model para construir un grafo."""
    graph_type: Literal["GT", "GC", "GUC"] = Field(
        ...,
        description="Tipo de grafo: GT (Transacciones), GC (Categorías), GUC (Usuario-Categoría)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "graph_type": "GT"
            }
        }


class TemporalGraphRequest(BaseModel):
    """Request model para construir grafo temporal."""
    time_window_days: int = Field(
        default=7,
        ge=1,
        le=365,
        description="Ventana de tiempo en días (1-365)"
    )


# ==================== Endpoints ====================

@router.post("/build", status_code=status.HTTP_201_CREATED)
def build_graph(
    request: GraphBuildRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Construye un grafo del tipo especificado desde las transacciones en la base de datos.

    Tipos de grafo soportados:
    - GT: Grafo de Transacciones - Conecta transacciones secuenciales del mismo usuario
    - GC: Grafo de Categorías - Conecta categorías basado en patrones de gasto
    - GUC: Grafo Usuario-Categoría - Grafo bipartito entre usuarios y categorías

    Args:
        request: Objeto con el tipo de grafo a construir
        db: Sesión de base de datos

    Returns:
        Grafo construido y estadísticas básicas

    Raises:
        HTTPException: Si ocurre un error al construir el grafo
    """
    try:
        graph_type = request.graph_type.upper()

        if graph_type == "GT":
            graph = graph_service.build_gt_from_db(db)
            description = "Grafo de Transacciones"
        elif graph_type == "GC":
            graph = graph_service.build_gc_from_db(db)
            description = "Grafo de Categorías"
        elif graph_type == "GUC":
            graph = graph_service.build_guc_from_db(db)
            description = "Grafo Usuario-Categoría"
        else:
            raise ValueError(f"Tipo de grafo inválido: {graph_type}")

        stats = graph_service.get_graph_statistics(graph)

        return {
            "message": f"{description} construido exitosamente",
            "graph_type": graph_type,
            "description": description,
            "graph": graph,
            "statistics": stats
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error construyendo grafo: {str(e)}"
        )


@router.get("/{graph_type}", status_code=status.HTTP_200_OK)
def get_graph(
    graph_type: Literal["GT", "GC", "GUC"],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtiene un grafo específico del tipo indicado.

    Args:
        graph_type: Tipo de grafo (GT, GC, GUC)
        db: Sesión de base de datos

    Returns:
        Grafo del tipo solicitado

    Raises:
        HTTPException: Si el tipo de grafo es inválido o ocurre error
    """
    try:
        graph_type = graph_type.upper()

        if graph_type == "GT":
            graph = graph_service.build_gt_from_db(db)
            description = "Grafo de Transacciones"
        elif graph_type == "GC":
            graph = graph_service.build_gc_from_db(db)
            description = "Grafo de Categorías"
        elif graph_type == "GUC":
            graph = graph_service.build_guc_from_db(db)
            description = "Grafo Usuario-Categoría"
        else:
            raise ValueError(f"Tipo de grafo inválido: {graph_type}")

        return {
            "graph_type": graph_type,
            "description": description,
            "graph": graph
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo grafo: {str(e)}"
        )


@router.get("/stats/all", status_code=status.HTTP_200_OK)
def get_all_graphs_stats(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtiene las estadísticas de todos los tipos de grafos disponibles.

    Args:
        db: Sesión de base de datos

    Returns:
        Estadísticas comparativas de GT, GC y GUC

    Raises:
        HTTPException: Si ocurre error al calcular estadísticas
    """
    try:
        stats = graph_service.compare_graph_types(db)

        return {
            "message": "Estadísticas de todos los grafos",
            "statistics": stats,
            "timestamp": None  # Podría agregarse timestamp si es necesario
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculando estadísticas: {str(e)}"
        )


@router.get("/stats/{graph_type}", status_code=status.HTTP_200_OK)
def get_graph_stats(
    graph_type: Literal["GT", "GC", "GUC"],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtiene las estadísticas de un grafo específico.

    Las estadísticas incluyen:
    - Número de nodos y aristas
    - Grado promedio
    - Densidad del grafo
    - Componentes conexas
    - Información de pesos (si aplica)

    Args:
        graph_type: Tipo de grafo (GT, GC, GUC)
        db: Sesión de base de datos

    Returns:
        Estadísticas detalladas del grafo solicitado

    Raises:
        HTTPException: Si el tipo de grafo es inválido o ocurre error
    """
    try:
        graph_type = graph_type.upper()

        if graph_type == "GT":
            stats = graph_service.get_gt_statistics(db)
        elif graph_type == "GC":
            stats = graph_service.get_gc_statistics(db)
        elif graph_type == "GUC":
            stats = graph_service.get_guc_statistics(db)
        else:
            raise ValueError(f"Tipo de grafo inválido: {graph_type}")

        return {
            "graph_type": graph_type,
            "statistics": stats
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculando estadísticas: {str(e)}"
        )


@router.get("/summary/overview", status_code=status.HTTP_200_OK)
def get_graphs_summary(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtiene un resumen general de los grafos disponibles.

    Incluye información de las transacciones, usuarios, categorías,
    y disponibilidad de cada tipo de grafo.

    Args:
        db: Sesión de base de datos

    Returns:
        Resumen de grafos y datos disponibles

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        summary = graph_service.get_graph_summary(db)

        return {
            "message": "Resumen de grafos disponibles",
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo resumen: {str(e)}"
        )


@router.post("/temporal/build", status_code=status.HTTP_201_CREATED)
def build_temporal_graph(
    request: TemporalGraphRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Construye un grafo temporal basado en una ventana de tiempo.

    Las transacciones que ocurren dentro de la ventana de tiempo
    especificada se conectan en el grafo temporal.

    Args:
        request: Objeto con la ventana de tiempo en días
        db: Sesión de base de datos

    Returns:
        Grafo temporal construido y estadísticas

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        graph = graph_service.build_temporal_graph_from_db(
            db,
            time_window_days=request.time_window_days
        )
        stats = graph_service.get_graph_statistics(graph)

        return {
            "message": "Grafo temporal construido exitosamente",
            "time_window_days": request.time_window_days,
            "graph": graph,
            "statistics": stats
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error construyendo grafo temporal: {str(e)}"
        )


@router.post("/weighted-categories/build", status_code=status.HTTP_201_CREATED)
def build_weighted_category_graph(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Construye un grafo de categorías con pesos basados en frecuencia de transición.

    Las aristas entre categorías tienen pesos que representan la frecuencia
    con que un usuario gasta en ambas categorías en secuencia.

    Args:
        db: Sesión de base de datos

    Returns:
        Grafo de categorías ponderado y estadísticas

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        graph = graph_service.build_weighted_category_graph_from_db(db)
        stats = graph_service.get_graph_statistics(graph)

        return {
            "message": "Grafo de categorías ponderado construido exitosamente",
            "graph": graph,
            "statistics": stats
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error construyendo grafo ponderado: {str(e)}"
        )
