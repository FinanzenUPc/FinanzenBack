"""
Algorithms Router - Endpoints para todos los algoritmos de grafos y optimización
Incluye: BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, MST (Prim/Kruskal), DP (Knapsack)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Tuple, Optional
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.services.algorithms_service import algorithms_service

router = APIRouter(prefix="/algorithms", tags=["Algorithms"])


# ==================== Pydantic Models for BFS ====================

class BFSRequest(BaseModel):
    """Request model para BFS."""
    graph: Dict[int, List[int]] = Field(
        ...,
        description="Grafo representado como diccionario de adyacencia {nodo: [vecinos]}"
    )
    start: int = Field(
        ...,
        description="Nodo inicial para la búsqueda BFS"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "graph": {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]},
                "start": 0
            }
        }


class BFSPathRequest(BaseModel):
    """Request model para encontrar camino más corto con BFS."""
    graph: Dict[int, List[int]] = Field(...)
    start: int = Field(...)
    end: int = Field(...)


# ==================== Pydantic Models for DFS ====================

class DFSRequest(BaseModel):
    """Request model para DFS."""
    graph: Dict[int, List[int]] = Field(...)
    start: int = Field(...)


class DFSPathRequest(BaseModel):
    """Request model para encontrar todos los caminos con DFS."""
    graph: Dict[int, List[int]] = Field(...)
    start: int = Field(...)
    end: int = Field(...)


# ==================== Pydantic Models for Dijkstra ====================

class DijkstraRequest(BaseModel):
    """Request model para Dijkstra."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(
        ...,
        description="Grafo con pesos {nodo: [(vecino, peso), ...]}"
    )
    start: int = Field(...)


class DijkstraPathRequest(BaseModel):
    """Request model para camino más corto con Dijkstra."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(...)
    start: int = Field(...)
    end: int = Field(...)


# ==================== Pydantic Models for Bellman-Ford ====================

class BellmanFordRequest(BaseModel):
    """Request model para Bellman-Ford."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(...)
    start: int = Field(...)


class BellmanFordPathRequest(BaseModel):
    """Request model para camino más corto con Bellman-Ford."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(...)
    start: int = Field(...)
    end: int = Field(...)


# ==================== Pydantic Models for Floyd-Warshall ====================

class FloydWarshallRequest(BaseModel):
    """Request model para Floyd-Warshall."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(
        ...,
        description="Grafo con pesos para calcular todos los caminos más cortos"
    )


class FloydWarshallPathRequest(BaseModel):
    """Request model para camino más corto con Floyd-Warshall."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(...)
    start: int = Field(...)
    end: int = Field(...)


# ==================== Pydantic Models for MST ====================

class KruskalRequest(BaseModel):
    """Request model para Kruskal MST."""
    edges: List[Tuple[int, int, float]] = Field(
        ...,
        description="Lista de aristas como (u, v, peso)"
    )
    num_vertices: int = Field(
        ...,
        description="Número de vértices en el grafo"
    )


class KruskalGraphRequest(BaseModel):
    """Request model para Kruskal desde representación de grafo."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(...)
    num_vertices: int = Field(...)


class PrimRequest(BaseModel):
    """Request model para Prim MST."""
    edges: List[Tuple[int, int, float]] = Field(...)
    num_vertices: int = Field(...)
    start: int = Field(
        default=0,
        description="Nodo inicial para Prim"
    )


class PrimGraphRequest(BaseModel):
    """Request model para Prim desde representación de grafo."""
    graph: Dict[int, List[Tuple[int, float]]] = Field(...)
    num_vertices: int = Field(...)
    start: int = Field(default=0)


# ==================== Pydantic Models for Dynamic Programming ====================

class Knapsack01Request(BaseModel):
    """Request model para Knapsack 0/1."""
    weights: List[int] = Field(
        ...,
        description="Pesos de los items"
    )
    values: List[int] = Field(
        ...,
        description="Valores de los items"
    )
    capacity: int = Field(
        ...,
        ge=1,
        description="Capacidad de la mochila"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "weights": [2, 3, 4, 5],
                "values": [3, 4, 5, 6],
                "capacity": 5
            }
        }


class KnapsackUnboundedRequest(BaseModel):
    """Request model para Knapsack sin límite."""
    weights: List[int] = Field(...)
    values: List[int] = Field(...)
    capacity: int = Field(ge=1)


class KnapsackFractionalRequest(BaseModel):
    """Request model para Knapsack fraccionaria."""
    weights: List[float] = Field(...)
    values: List[float] = Field(...)
    capacity: float = Field(gt=0)


class SubsetSumRequest(BaseModel):
    """Request model para Subset Sum."""
    numbers: List[int] = Field(
        ...,
        description="Lista de números"
    )
    target: int = Field(
        ...,
        description="Suma objetivo"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "numbers": [3, 34, 4, 12, 5, 2],
                "target": 9
            }
        }


# ==================== BFS Endpoints ====================

@router.post("/bfs", status_code=status.HTTP_200_OK)
def execute_bfs(request: BFSRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Búsqueda en Amplitud (BFS).

    Complejidad: O(V + E)

    Args:
        request: Grafo y nodo inicial

    Returns:
        Orden de visita, distancias y información de padres

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.bfs_traversal(request.graph, request.start)
        return {
            "algorithm": "Breadth-First Search (BFS)",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando BFS: {str(e)}"
        )


@router.post("/bfs/shortest-path", status_code=status.HTTP_200_OK)
def bfs_shortest_path(request: BFSPathRequest) -> Dict[str, Any]:
    """
    Encuentra el camino más corto entre dos nodos usando BFS.

    Complejidad: O(V + E)

    Args:
        request: Grafo, nodo inicio y nodo final

    Returns:
        Camino más corto y su longitud

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.bfs_shortest_path(
            request.graph,
            request.start,
            request.end
        )
        return {
            "algorithm": "BFS Shortest Path",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en BFS shortest path: {str(e)}"
        )


@router.post("/bfs/levels", status_code=status.HTTP_200_OK)
def bfs_levels(request: BFSRequest) -> Dict[str, Any]:
    """
    Organiza nodos por niveles usando BFS.

    Complejidad: O(V + E)

    Args:
        request: Grafo y nodo inicial

    Returns:
        Nodos organizados por niveles desde el nodo inicial

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.bfs_levels(request.graph, request.start)
        return {
            "algorithm": "BFS Levels",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en BFS levels: {str(e)}"
        )


# ==================== DFS Endpoints ====================

@router.post("/dfs", status_code=status.HTTP_200_OK)
def execute_dfs(request: DFSRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Búsqueda en Profundidad (DFS) iterativo.

    Complejidad: O(V + E)

    Args:
        request: Grafo y nodo inicial

    Returns:
        Orden de visita y estadísticas

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.dfs_traversal(request.graph, request.start)
        return {
            "algorithm": "Depth-First Search (DFS)",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando DFS: {str(e)}"
        )


@router.post("/dfs/recursive", status_code=status.HTTP_200_OK)
def dfs_recursive(request: DFSRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo DFS de forma recursiva.

    Complejidad: O(V + E)

    Args:
        request: Grafo y nodo inicial

    Returns:
        Orden de visita usando DFS recursivo

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.dfs_recursive_traversal(request.graph, request.start)
        return {
            "algorithm": "DFS (Recursive)",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en DFS recursivo: {str(e)}"
        )


@router.post("/dfs/all-paths", status_code=status.HTTP_200_OK)
def dfs_all_paths(request: DFSPathRequest) -> Dict[str, Any]:
    """
    Encuentra todos los caminos entre dos nodos usando DFS.

    Complejidad: O(V^V) en el peor caso

    Args:
        request: Grafo, nodo inicio y nodo final

    Returns:
        Todos los caminos, cantidad y camino más corto

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.dfs_all_paths(
            request.graph,
            request.start,
            request.end
        )
        return {
            "algorithm": "DFS All Paths",
            "complexity": "O(V^V) worst case",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en DFS all paths: {str(e)}"
        )


@router.post("/dfs/detect-cycle", status_code=status.HTTP_200_OK)
def detect_cycle(request: DFSRequest) -> Dict[str, Any]:
    """
    Detecta ciclos en un grafo dirigido usando DFS.

    Complejidad: O(V + E)

    Args:
        request: Grafo

    Returns:
        Indica si el grafo contiene ciclos

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.detect_cycle(request.graph)
        return {
            "algorithm": "Cycle Detection (DFS)",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error detectando ciclos: {str(e)}"
        )


@router.post("/dfs/topological-sort", status_code=status.HTTP_200_OK)
def topological_sort(request: DFSRequest) -> Dict[str, Any]:
    """
    Realiza ordenamiento topológico de un grafo dirigido acíclico (DAG).

    Complejidad: O(V + E)

    Args:
        request: Grafo dirigido acíclico

    Returns:
        Orden topológico o error si contiene ciclos

    Raises:
        HTTPException: Si el grafo contiene ciclos
    """
    try:
        result = algorithms_service.topological_sort(request.graph)
        return {
            "algorithm": "Topological Sort (DFS)",
            "complexity": "O(V + E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en ordenamiento topológico: {str(e)}"
        )


# ==================== Dijkstra Endpoints ====================

@router.post("/dijkstra", status_code=status.HTTP_200_OK)
def execute_dijkstra(request: DijkstraRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Dijkstra para encontrar caminos más cortos.

    Calcula los caminos más cortos desde un nodo inicial a todos los demás.

    Complejidad: O((V + E) log V) con heap

    Args:
        request: Grafo con pesos y nodo inicial

    Returns:
        Distancias y padres de todos los nodos alcanzables

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.dijkstra_shortest_paths(request.graph, request.start)
        return {
            "algorithm": "Dijkstra Shortest Paths",
            "complexity": "O((V + E) log V)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando Dijkstra: {str(e)}"
        )


@router.post("/dijkstra/path", status_code=status.HTTP_200_OK)
def dijkstra_path(request: DijkstraPathRequest) -> Dict[str, Any]:
    """
    Encuentra el camino más corto entre dos nodos específicos usando Dijkstra.

    Complejidad: O((V + E) log V) con heap

    Args:
        request: Grafo, nodo inicio y nodo final

    Returns:
        Camino más corto y su distancia

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.dijkstra_path(request.graph, request.start, request.end)
        return {
            "algorithm": "Dijkstra Path",
            "complexity": "O((V + E) log V)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Dijkstra path: {str(e)}"
        )


@router.post("/dijkstra/all-paths", status_code=status.HTTP_200_OK)
def dijkstra_all_paths(request: DijkstraRequest) -> Dict[str, Any]:
    """
    Encuentra todos los caminos más cortos desde un nodo inicial usando Dijkstra.

    Complejidad: O((V + E) log V) con heap

    Args:
        request: Grafo con pesos y nodo inicial

    Returns:
        Todos los caminos más cortos desde el nodo inicial

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.dijkstra_all_paths_from(request.graph, request.start)
        return {
            "algorithm": "Dijkstra All Paths",
            "complexity": "O((V + E) log V)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Dijkstra all paths: {str(e)}"
        )


# ==================== Bellman-Ford Endpoints ====================

@router.post("/bellman-ford", status_code=status.HTTP_200_OK)
def execute_bellman_ford(request: BellmanFordRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Bellman-Ford para encontrar caminos más cortos.

    Funciona con pesos negativos y detecta ciclos negativos.

    Complejidad: O(V * E)

    Args:
        request: Grafo con pesos (puede tener pesos negativos) y nodo inicial

    Returns:
        Distancias, padres y detección de ciclos negativos

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.bellman_ford_shortest_paths(request.graph, request.start)
        return {
            "algorithm": "Bellman-Ford Shortest Paths",
            "complexity": "O(V * E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando Bellman-Ford: {str(e)}"
        )


@router.post("/bellman-ford/path", status_code=status.HTTP_200_OK)
def bellman_ford_path(request: BellmanFordPathRequest) -> Dict[str, Any]:
    """
    Encuentra el camino más corto entre dos nodos usando Bellman-Ford.

    Puede detectar ciclos negativos en el grafo.

    Complejidad: O(V * E)

    Args:
        request: Grafo, nodo inicio y nodo final

    Returns:
        Camino más corto y su distancia

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.bellman_ford_path(request.graph, request.start, request.end)
        return {
            "algorithm": "Bellman-Ford Path",
            "complexity": "O(V * E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Bellman-Ford path: {str(e)}"
        )


# ==================== Floyd-Warshall Endpoints ====================

@router.post("/floyd-warshall", status_code=status.HTTP_200_OK)
def execute_floyd_warshall(request: FloydWarshallRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Floyd-Warshall para encontrar caminos más cortos entre todos los pares.

    Complejidad: O(V³)

    Args:
        request: Grafo con pesos

    Returns:
        Matriz de distancias y caminos entre todos los pares de nodos

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.floyd_warshall_all_pairs(request.graph)
        return {
            "algorithm": "Floyd-Warshall All Pairs",
            "complexity": "O(V³)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando Floyd-Warshall: {str(e)}"
        )


@router.post("/floyd-warshall/path", status_code=status.HTTP_200_OK)
def floyd_warshall_path(request: FloydWarshallPathRequest) -> Dict[str, Any]:
    """
    Encuentra el camino más corto entre dos nodos usando Floyd-Warshall.

    Complejidad: O(V³) para calcular todas las distancias

    Args:
        request: Grafo, nodo inicio y nodo final

    Returns:
        Camino más corto y su distancia

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.floyd_warshall_path(request.graph, request.start, request.end)
        return {
            "algorithm": "Floyd-Warshall Path",
            "complexity": "O(V³)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Floyd-Warshall path: {str(e)}"
        )


# ==================== MST: Kruskal Endpoints ====================

@router.post("/mst/kruskal", status_code=status.HTTP_200_OK)
def execute_kruskal(request: KruskalRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Kruskal para encontrar el Árbol de Expansión Mínima.

    Ordenación de aristas por peso y selección mediante Union-Find.

    Complejidad: O(E log E)

    Args:
        request: Lista de aristas (u, v, peso) y número de vértices

    Returns:
        Aristas del MST y peso total

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.kruskal_mst(request.edges, request.num_vertices)
        return {
            "algorithm": "Kruskal MST",
            "complexity": "O(E log E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando Kruskal: {str(e)}"
        )


@router.post("/mst/kruskal-graph", status_code=status.HTTP_200_OK)
def kruskal_from_graph(request: KruskalGraphRequest) -> Dict[str, Any]:
    """
    Ejecuta Kruskal desde una representación de grafo en diccionario.

    Complejidad: O(E log E)

    Args:
        request: Grafo con pesos y número de vértices

    Returns:
        MST encontrado

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.kruskal_mst_from_graph(request.graph, request.num_vertices)
        return {
            "algorithm": "Kruskal MST from Graph",
            "complexity": "O(E log E)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Kruskal from graph: {str(e)}"
        )


# ==================== MST: Prim Endpoints ====================

@router.post("/mst/prim", status_code=status.HTTP_200_OK)
def execute_prim(request: PrimRequest) -> Dict[str, Any]:
    """
    Ejecuta el algoritmo de Prim para encontrar el Árbol de Expansión Mínima.

    Selecciona aristas de menor peso desde nodos visitados.

    Complejidad: O(E log V) con heap

    Args:
        request: Lista de aristas, número de vértices y nodo inicial

    Returns:
        Aristas del MST y peso total

    Raises:
        HTTPException: Si el grafo es inválido
    """
    try:
        result = algorithms_service.prim_mst(
            request.edges,
            request.num_vertices,
            request.start
        )
        return {
            "algorithm": "Prim MST",
            "complexity": "O(E log V)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando Prim: {str(e)}"
        )


@router.post("/mst/prim-graph", status_code=status.HTTP_200_OK)
def prim_from_graph(request: PrimGraphRequest) -> Dict[str, Any]:
    """
    Ejecuta Prim desde una representación de grafo en diccionario.

    Complejidad: O(E log V) con heap

    Args:
        request: Grafo con pesos, número de vértices y nodo inicial

    Returns:
        MST encontrado

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.prim_mst_from_graph(
            request.graph,
            request.num_vertices,
            request.start
        )
        return {
            "algorithm": "Prim MST from Graph",
            "complexity": "O(E log V)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Prim from graph: {str(e)}"
        )


# ==================== Dynamic Programming: Knapsack Endpoints ====================

@router.post("/dp-mochila/01", status_code=status.HTTP_200_OK)
def knapsack_01(request: Knapsack01Request) -> Dict[str, Any]:
    """
    Resuelve el problema de la mochila 0/1 usando programación dinámica.

    Cada item puede incluirse una sola vez (0 o 1).

    Complejidad: O(n * W) donde W es la capacidad

    Args:
        request: Pesos, valores y capacidad de la mochila

    Returns:
        Valor máximo e items seleccionados

    Raises:
        HTTPException: Si los datos son inválidos
    """
    try:
        if len(request.weights) != len(request.values):
            raise ValueError("Pesos y valores deben tener la misma longitud")

        result = algorithms_service.knapsack_01_problem(
            request.weights,
            request.values,
            request.capacity
        )
        return {
            "algorithm": "0/1 Knapsack",
            "complexity": "O(n * W)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Knapsack 0/1: {str(e)}"
        )


@router.post("/dp-mochila/unbounded", status_code=status.HTTP_200_OK)
def knapsack_unbounded(request: KnapsackUnboundedRequest) -> Dict[str, Any]:
    """
    Resuelve el problema de la mochila sin límite (unbounded knapsack).

    Cada item puede incluirse múltiples veces.

    Complejidad: O(n * W) donde W es la capacidad

    Args:
        request: Pesos, valores y capacidad de la mochila

    Returns:
        Valor máximo

    Raises:
        HTTPException: Si los datos son inválidos
    """
    try:
        if len(request.weights) != len(request.values):
            raise ValueError("Pesos y valores deben tener la misma longitud")

        result = algorithms_service.knapsack_unbounded_problem(
            request.weights,
            request.values,
            request.capacity
        )
        return {
            "algorithm": "Unbounded Knapsack",
            "complexity": "O(n * W)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Unbounded Knapsack: {str(e)}"
        )


@router.post("/dp-mochila/fractional", status_code=status.HTTP_200_OK)
def knapsack_fractional(request: KnapsackFractionalRequest) -> Dict[str, Any]:
    """
    Resuelve el problema de la mochila fraccionaria usando greedy.

    Se pueden incluir fracciones de items.

    Complejidad: O(n log n)

    Args:
        request: Pesos, valores y capacidad de la mochila

    Returns:
        Valor máximo y fracciones de items incluidas

    Raises:
        HTTPException: Si los datos son inválidos
    """
    try:
        if len(request.weights) != len(request.values):
            raise ValueError("Pesos y valores deben tener la misma longitud")

        result = algorithms_service.knapsack_fractional_problem(
            request.weights,
            request.values,
            request.capacity
        )
        return {
            "algorithm": "Fractional Knapsack",
            "complexity": "O(n log n)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Fractional Knapsack: {str(e)}"
        )


# ==================== Dynamic Programming: Subset Sum Endpoint ====================

@router.post("/dp-mochila/subset-sum", status_code=status.HTTP_200_OK)
def subset_sum(request: SubsetSumRequest) -> Dict[str, Any]:
    """
    Resuelve el problema de suma de subconjunto (Subset Sum).

    Determina si existe un subconjunto cuya suma sea igual al objetivo.

    Complejidad: O(n * target)

    Args:
        request: Lista de números y suma objetivo

    Returns:
        Indica si es posible y el subconjunto encontrado

    Raises:
        HTTPException: Si los datos son inválidos
    """
    try:
        result = algorithms_service.subset_sum_problem(request.numbers, request.target)
        return {
            "algorithm": "Subset Sum",
            "complexity": "O(n * target)",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en Subset Sum: {str(e)}"
        )


# ==================== Informational Endpoints ====================

@router.get("/info/complexity", status_code=status.HTTP_200_OK)
def get_algorithms_complexity() -> Dict[str, Any]:
    """
    Obtiene información sobre la complejidad de todos los algoritmos disponibles.

    Returns:
        Dict con complejidad temporal y espacial de cada algoritmo
    """
    try:
        complexity_info = algorithms_service.get_algorithm_complexity_info()
        return {
            "message": "Información de complejidad de algoritmos",
            "algorithms": complexity_info
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo información: {str(e)}"
        )


@router.post("/compare/shortest-paths", status_code=status.HTTP_200_OK)
def compare_shortest_paths(request: DijkstraPathRequest) -> Dict[str, Any]:
    """
    Compara los resultados de diferentes algoritmos de camino más corto.

    Ejecuta Dijkstra, Bellman-Ford y Floyd-Warshall sobre el mismo problema.

    Args:
        request: Grafo, nodo inicio y nodo final

    Returns:
        Resultados de los tres algoritmos para comparación

    Raises:
        HTTPException: Si ocurre error
    """
    try:
        result = algorithms_service.compare_shortest_path_algorithms(
            request.graph,
            request.start,
            request.end
        )
        return {
            "message": "Comparación de algoritmos de camino más corto",
            "comparison": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en comparación: {str(e)}"
        )
