"""
Dijkstra's Algorithm - Camino más corto con pesos positivos
Complejidad: O((V + E) log V) con heap
"""
import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra(graph: Dict[int, List[Tuple[int, float]]], start: int) -> Dict[str, any]:
    """
    Algoritmo de Dijkstra para encontrar caminos más cortos.

    Args:
        graph: Grafo representado como {nodo: [(vecino, peso), ...]}
        start: Nodo inicial

    Returns:
        Dict con distancias y padres
    """
    distances = {start: 0}
    parents = {start: None}
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                distance = current_dist + weight

                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parents[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))

    return {
        "distances": distances,
        "parents": parents
    }


def dijkstra_path(graph: Dict[int, List[Tuple[int, float]]], start: int, end: int) -> Optional[Dict[str, any]]:
    """
    Encuentra el camino más corto entre dos nodos usando Dijkstra.

    Args:
        graph: Grafo con pesos
        start: Nodo inicial
        end: Nodo final

    Returns:
        Dict con camino y distancia total, o None si no existe
    """
    result = dijkstra(graph, start)
    distances = result["distances"]
    parents = result["parents"]

    if end not in distances:
        return None

    # Reconstruir camino
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = parents.get(current)

    path.reverse()

    return {
        "path": path,
        "distance": distances[end],
        "all_distances": distances
    }


def dijkstra_all_paths(graph: Dict[int, List[Tuple[int, float]]], start: int) -> Dict[int, Dict[str, any]]:
    """
    Encuentra todos los caminos más cortos desde un nodo inicial.

    Args:
        graph: Grafo con pesos
        start: Nodo inicial

    Returns:
        Dict con información de todos los caminos
    """
    result = dijkstra(graph, start)
    distances = result["distances"]
    parents = result["parents"]

    paths = {}

    for end_node in distances:
        if end_node == start:
            paths[end_node] = {
                "path": [start],
                "distance": 0
            }
        else:
            path = []
            current = end_node

            while current is not None:
                path.append(current)
                current = parents.get(current)

            path.reverse()

            paths[end_node] = {
                "path": path,
                "distance": distances[end_node]
            }

    return paths
