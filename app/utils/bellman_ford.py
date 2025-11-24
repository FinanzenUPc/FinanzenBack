"""
Bellman-Ford Algorithm - Camino más corto con pesos negativos
Complejidad: O(V * E)
"""
from typing import Dict, List, Tuple, Optional


def bellman_ford(graph: Dict[int, List[Tuple[int, float]]], start: int, num_vertices: int) -> Optional[Dict[str, any]]:
    """
    Algoritmo de Bellman-Ford para encontrar caminos más cortos.
    Funciona con pesos negativos y detecta ciclos negativos.

    Args:
        graph: Grafo representado como {nodo: [(vecino, peso), ...]}
        start: Nodo inicial
        num_vertices: Número total de vértices

    Returns:
        Dict con distancias y padres, o None si hay ciclo negativo
    """
    # Inicializar distancias
    distances = {i: float('inf') for i in range(num_vertices)}
    distances[start] = 0
    parents = {i: None for i in range(num_vertices)}

    # Relajar todas las aristas V-1 veces
    for _ in range(num_vertices - 1):
        updated = False
        for node in graph:
            if node in distances and distances[node] != float('inf'):
                for neighbor, weight in graph[node]:
                    if distances[node] + weight < distances[neighbor]:
                        distances[neighbor] = distances[node] + weight
                        parents[neighbor] = node
                        updated = True

        # Optimización: si no hubo actualizaciones, terminar
        if not updated:
            break

    # Verificar ciclos negativos
    has_negative_cycle = False
    for node in graph:
        if node in distances and distances[node] != float('inf'):
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    has_negative_cycle = True
                    break
        if has_negative_cycle:
            break

    if has_negative_cycle:
        return None

    return {
        "distances": {k: v for k, v in distances.items() if v != float('inf')},
        "parents": parents,
        "has_negative_cycle": False
    }


def bellman_ford_path(graph: Dict[int, List[Tuple[int, float]]], start: int, end: int, num_vertices: int) -> Optional[Dict[str, any]]:
    """
    Encuentra el camino más corto usando Bellman-Ford.

    Args:
        graph: Grafo con pesos (pueden ser negativos)
        start: Nodo inicial
        end: Nodo final
        num_vertices: Número total de vértices

    Returns:
        Dict con camino y distancia, o None si hay ciclo negativo o no existe camino
    """
    result = bellman_ford(graph, start, num_vertices)

    if result is None:
        return {"error": "Ciclo negativo detectado"}

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
        "distance": distances[end]
    }


def detect_negative_cycle(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int) -> bool:
    """
    Detecta si existe un ciclo negativo en el grafo.

    Args:
        graph: Grafo con pesos
        num_vertices: Número total de vértices

    Returns:
        True si hay ciclo negativo, False en caso contrario
    """
    # Ejecutar desde el nodo 0
    result = bellman_ford(graph, 0, num_vertices)

    return result is None
