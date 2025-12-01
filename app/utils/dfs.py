"""
DFS (Depth-First Search) Algorithm
Complejidad: O(V + E)
"""
from typing import Dict, List, Set, Optional


def dfs(graph: Dict[int, List[int]], start: int) -> Dict[str, any]:
    """
    Ejecuta DFS desde un nodo inicial (iterativo).

    Args:
        graph: Grafo representado como diccionario de adyacencia
        start: Nodo inicial

    Returns:
        Dict con orden de visita y tiempos
    """
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            order.append(node)

            if node in graph:
                # Agregar vecinos en orden inverso para mantener orden correcto
                for neighbor in reversed(graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

    return {
        "order": order,
        "visited_count": len(visited)
    }


def dfs_recursive(graph: Dict[int, List[int]], start: int, visited: Optional[Set[int]] = None) -> List[int]:
    """
    Ejecuta DFS recursivamente.

    Args:
        graph: Grafo representado como diccionario de adyacencia
        start: Nodo inicial
        visited: Set de nodos visitados

    Returns:
        Lista con orden de visita
    """
    if visited is None:
        visited = set()

    visited.add(start)
    order = [start]

    if start in graph:
        for neighbor in graph[start]:
            if neighbor not in visited:
                order.extend(dfs_recursive(graph, neighbor, visited))

    return order


def dfs_paths(graph: Dict[int, List[int]], start: int, end: int, path: Optional[List[int]] = None) -> List[List[int]]:
    """
    Encuentra todos los caminos entre dos nodos usando DFS.

    Args:
        graph: Grafo representado como diccionario de adyacencia
        start: Nodo inicial
        end: Nodo final
        path: Camino actual (recursivo)

    Returns:
        Lista de todos los caminos posibles
    """
    if path is None:
        path = []

    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for neighbor in graph[start]:
        if neighbor not in path:  # Evitar ciclos
            new_paths = dfs_paths(graph, neighbor, end, path)
            paths.extend(new_paths)

    return paths


def detect_cycle_dfs(graph: Dict[int, List[int]]) -> Dict[str, any]:
    """
    Detecta ciclos en un grafo dirigido usando DFS y devuelve el ciclo si existe.

    Args:
        graph: Grafo representado como diccionario de adyacencia

    Returns:
        Dict con has_cycle (bool) y cycle (lista de nodos del ciclo)
    """
    visited = set()
    rec_stack = set()
    path = []
    cycle_found = []

    def find_cycle(node: int) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if find_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Encontramos un ciclo - extraer el ciclo del path
                    cycle_start_idx = path.index(neighbor)
                    cycle_found.extend(path[cycle_start_idx:])
                    cycle_found.append(neighbor)  # Cerrar el ciclo
                    return True

        path.pop()
        rec_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if find_cycle(node):
                return {
                    'has_cycle': True,
                    'cycle': cycle_found
                }

    return {
        'has_cycle': False,
        'cycle': []
    }


def topological_sort_dfs(graph: Dict[int, List[int]]) -> Optional[List[int]]:
    """
    Ordenamiento topológico usando DFS.

    Args:
        graph: Grafo dirigido acíclico (DAG)

    Returns:
        Lista con orden topológico o None si hay ciclo
    """
    cycle_result = detect_cycle_dfs(graph)
    if cycle_result['has_cycle']:
        return None

    visited = set()
    stack = []

    def dfs_util(node: int):
        visited.add(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs_util(neighbor)

        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs_util(node)

    return stack[::-1]
