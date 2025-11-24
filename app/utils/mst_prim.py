"""
Prim's Algorithm - Minimum Spanning Tree
Complejidad: O((V + E) log V) con heap
"""
import heapq
from typing import Dict, List, Tuple, Optional


def prim(graph: Dict[int, List[Tuple[int, float]]], start: int = 0) -> Dict[str, any]:
    """
    Algoritmo de Prim para encontrar el Árbol de Expansión Mínima.

    Args:
        graph: Grafo representado como {nodo: [(vecino, peso), ...]}
        start: Nodo inicial (por defecto 0)

    Returns:
        Dict con aristas del MST y peso total
    """
    visited = set()
    mst_edges = []
    total_weight = 0

    # Min heap: (peso, nodo_actual, nodo_padre)
    heap = [(0, start, None)]

    while heap:
        weight, node, parent = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        if parent is not None:
            mst_edges.append((parent, node, weight))
            total_weight += weight

        if node in graph:
            for neighbor, edge_weight in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(heap, (edge_weight, neighbor, node))

    return {
        "mst_edges": mst_edges,
        "total_weight": total_weight,
        "num_edges": len(mst_edges),
        "visited_nodes": len(visited)
    }


def prim_all_components(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int) -> Dict[str, any]:
    """
    Ejecuta Prim en todas las componentes conexas.

    Args:
        graph: Grafo con posibles componentes desconectadas
        num_vertices: Número total de vértices

    Returns:
        Dict con información de todos los MST
    """
    visited_global = set()
    all_msts = []
    total_weight = 0

    for start in range(num_vertices):
        if start not in visited_global:
            result = prim(graph, start)
            all_msts.append(result)
            total_weight += result["total_weight"]

            # Marcar nodos visitados
            for u, v, _ in result["mst_edges"]:
                visited_global.add(u)
                visited_global.add(v)
            visited_global.add(start)

    return {
        "num_components": len(all_msts),
        "msts": all_msts,
        "total_weight": total_weight
    }
