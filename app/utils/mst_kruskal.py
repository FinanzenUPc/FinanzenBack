"""
Kruskal's Algorithm - Minimum Spanning Tree
Complejidad: O(E log E)
"""
from typing import List, Tuple, Dict
from app.utils.union_find import UnionFind


def kruskal(edges: List[Tuple[int, int, float]], num_vertices: int) -> Dict[str, any]:
    """
    Algoritmo de Kruskal para encontrar el Árbol de Expansión Mínima.

    Args:
        edges: Lista de aristas como (u, v, peso)
        num_vertices: Número de vértices

    Returns:
        Dict con aristas del MST y peso total
    """
    # Ordenar aristas por peso
    sorted_edges = sorted(edges, key=lambda x: x[2])

    uf = UnionFind(num_vertices)
    mst_edges = []
    total_weight = 0

    for u, v, weight in sorted_edges:
        # Si u y v no están en el mismo componente, agregar arista
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight

            # MST completo cuando tenemos V-1 aristas
            if len(mst_edges) == num_vertices - 1:
                break

    return {
        "mst_edges": mst_edges,
        "total_weight": total_weight,
        "num_edges": len(mst_edges),
        "is_connected": len(mst_edges) == num_vertices - 1
    }


def kruskal_from_graph(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int) -> Dict[str, any]:
    """
    Kruskal desde representación de grafo.

    Args:
        graph: Grafo representado como {nodo: [(vecino, peso), ...]}
        num_vertices: Número de vértices

    Returns:
        Dict con información del MST
    """
    # Convertir grafo a lista de aristas
    edges = []
    seen = set()

    for u in graph:
        for v, weight in graph[u]:
            # Evitar duplicados en grafo no dirigido
            edge = tuple(sorted([u, v])) + (weight,)
            if edge[:2] not in seen:
                seen.add(edge[:2])
                edges.append(edge)

    return kruskal(edges, num_vertices)
