"""
Floyd-Warshall Algorithm - Todos los pares de caminos más cortos
Complejidad: O(V^3)
"""
from typing import Dict, List, Tuple, Optional


def floyd_warshall(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int) -> Dict[str, any]:
    """
    Algoritmo de Floyd-Warshall para encontrar todos los caminos más cortos.

    Args:
        graph: Grafo representado como {nodo: [(vecino, peso), ...]}
        num_vertices: Número total de vértices

    Returns:
        Dict con matriz de distancias y siguiente nodo en el camino
    """
    # Inicializar matrices
    INF = float('inf')
    dist = [[INF for _ in range(num_vertices)] for _ in range(num_vertices)]
    next_node = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]

    # Distancia de un nodo a sí mismo es 0
    for i in range(num_vertices):
        dist[i][i] = 0

    # Inicializar con aristas del grafo
    for u in graph:
        for v, weight in graph[u]:
            dist[u][v] = weight
            next_node[u][v] = v

    # Floyd-Warshall
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return {
        "distances": dist,
        "next": next_node
    }


def reconstruct_path_fw(next_matrix: List[List[Optional[int]]], start: int, end: int) -> Optional[List[int]]:
    """
    Reconstruye el camino usando la matriz de siguiente nodo.

    Args:
        next_matrix: Matriz de siguiente nodo de Floyd-Warshall
        start: Nodo inicial
        end: Nodo final

    Returns:
        Lista con el camino o None si no existe
    """
    if next_matrix[start][end] is None:
        return None

    path = [start]
    current = start

    while current != end:
        current = next_matrix[current][end]
        if current is None:
            return None
        path.append(current)

    return path


def floyd_warshall_with_paths(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int) -> Dict[str, any]:
    """
    Floyd-Warshall que también devuelve los caminos.

    Args:
        graph: Grafo con pesos
        num_vertices: Número total de vértices

    Returns:
        Dict con distancias y todos los caminos
    """
    result = floyd_warshall(graph, num_vertices)
    dist = result["distances"]
    next_matrix = result["next"]

    paths = {}
    for i in range(num_vertices):
        paths[i] = {}
        for j in range(num_vertices):
            if i != j and dist[i][j] != float('inf'):
                path = reconstruct_path_fw(next_matrix, i, j)
                paths[i][j] = {
                    "path": path,
                    "distance": dist[i][j]
                }

    return {
        "distances": dist,
        "paths": paths
    }


def has_negative_cycle_fw(dist: List[List[float]], num_vertices: int) -> bool:
    """
    Detecta si hay ciclo negativo en el resultado de Floyd-Warshall.

    Args:
        dist: Matriz de distancias
        num_vertices: Número de vértices

    Returns:
        True si hay ciclo negativo
    """
    for i in range(num_vertices):
        if dist[i][i] < 0:
            return True
    return False
