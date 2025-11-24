"""
BFS (Breadth-First Search) Algorithm
Complejidad: O(V + E)
"""
from collections import deque
from typing import Dict, List, Set, Optional


def bfs(graph: Dict[int, List[int]], start: int) -> Dict[str, any]:
    """
    Ejecuta BFS desde un nodo inicial.

    Args:
        graph: Grafo representado como diccionario de adyacencia
        start: Nodo inicial

    Returns:
        Dict con orden de visita, distancias y padres
    """
    visited = set()
    queue = deque([start])
    visited.add(start)

    order = []
    distances = {start: 0}
    parents = {start: None}

    while queue:
        node = queue.popleft()
        order.append(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    distances[neighbor] = distances[node] + 1
                    parents[neighbor] = node

    return {
        "order": order,
        "distances": distances,
        "parents": parents,
        "visited_count": len(visited)
    }


def bfs_shortest_path(graph: Dict[int, List[int]], start: int, end: int) -> Optional[List[int]]:
    """
    Encuentra el camino más corto usando BFS.

    Args:
        graph: Grafo representado como diccionario de adyacencia
        start: Nodo inicial
        end: Nodo final

    Returns:
        Lista con el camino más corto o None si no existe
    """
    if start == end:
        return [start]

    visited = set([start])
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        if node in graph:
            for neighbor in graph[node]:
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

    return None


def bfs_levels(graph: Dict[int, List[int]], start: int) -> Dict[int, List[int]]:
    """
    Devuelve los nodos organizados por niveles.

    Args:
        graph: Grafo representado como diccionario de adyacencia
        start: Nodo inicial

    Returns:
        Dict con niveles y sus nodos
    """
    visited = set([start])
    queue = deque([(start, 0)])
    levels = {0: [start]}

    while queue:
        node, level = queue.popleft()

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))

                    if level + 1 not in levels:
                        levels[level + 1] = []
                    levels[level + 1].append(neighbor)

    return levels
