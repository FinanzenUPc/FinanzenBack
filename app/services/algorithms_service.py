"""
Algorithms Service - Envoltura de todos los algoritmos de grafos
Incluye: BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, MST, DP
"""
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session

# Importar funciones de los algoritmos
from app.utils.bfs import bfs, bfs_shortest_path, bfs_levels
from app.utils.dfs import dfs, dfs_recursive, dfs_paths, detect_cycle_dfs, topological_sort_dfs
from app.utils.dijkstra import dijkstra, dijkstra_path, dijkstra_all_paths
from app.utils.bellman_ford import bellman_ford, bellman_ford_path
from app.utils.floyd_warshall import floyd_warshall, floyd_warshall_with_paths
from app.utils.mst_kruskal import kruskal, kruskal_from_graph
from app.utils.mst_prim import prim, prim
from app.utils.dp_mochila import (
    knapsack_01, knapsack_unbounded, knapsack_fractional, subset_sum
)


class AlgorithmsService:
    """Servicio que encapsula todos los algoritmos de grafos y problemas de optimización."""

    # ==================== BFS Algorithms ====================

    @staticmethod
    def bfs_traversal(graph: Dict[int, List[int]], start: int) -> Dict[str, Any]:
        """
        Ejecuta BFS desde un nodo inicial.

        Complejidad: O(V + E)

        Args:
            graph: Grafo representado como diccionario de adyacencia
            start: Nodo inicial

        Returns:
            Dict con orden de visita, distancias y información sobre padres
        """
        return bfs(graph, start)

    @staticmethod
    def bfs_shortest_path(graph: Dict[int, List[int]], start: int, end: int) -> Optional[List[int]]:
        """
        Encuentra el camino más corto entre dos nodos usando BFS.

        Complejidad: O(V + E)

        Args:
            graph: Grafo representado como diccionario de adyacencia
            start: Nodo inicial
            end: Nodo final

        Returns:
            Lista con el camino más corto o None si no existe
        """
        result = bfs_shortest_path(graph, start, end)
        return {
            'path': result,
            'exists': result is not None,
            'length': len(result) - 1 if result else 0
        }

    @staticmethod
    def bfs_levels(graph: Dict[int, List[int]], start: int) -> Dict[int, List[int]]:
        """
        Devuelve los nodos organizados por niveles usando BFS.

        Complejidad: O(V + E)

        Args:
            graph: Grafo representado como diccionario de adyacencia
            start: Nodo inicial

        Returns:
            Dict con niveles y sus nodos
        """
        return bfs_levels(graph, start)

    # ==================== DFS Algorithms ====================

    @staticmethod
    def dfs_traversal(graph: Dict[int, List[int]], start: int) -> Dict[str, Any]:
        """
        Ejecuta DFS desde un nodo inicial (iterativo).

        Complejidad: O(V + E)

        Args:
            graph: Grafo representado como diccionario de adyacencia
            start: Nodo inicial

        Returns:
            Dict con orden de visita y estadísticas
        """
        return dfs(graph, start)

    @staticmethod
    def dfs_recursive_traversal(graph: Dict[int, List[int]], start: int) -> List[int]:
        """
        Ejecuta DFS recursivamente desde un nodo inicial.

        Complejidad: O(V + E)

        Args:
            graph: Grafo representado como diccionario de adyacencia
            start: Nodo inicial

        Returns:
            Lista con orden de visita
        """
        return {
            'order': dfs_recursive(graph, start),
            'algorithm': 'DFS (Recursive)'
        }

    @staticmethod
    def dfs_all_paths(graph: Dict[int, List[int]], start: int, end: int) -> Dict[str, Any]:
        """
        Encuentra todos los caminos entre dos nodos usando DFS.

        Complejidad: O(V^V) en el peor caso

        Args:
            graph: Grafo representado como diccionario de adyacencia
            start: Nodo inicial
            end: Nodo final

        Returns:
            Dict con todos los caminos encontrados
        """
        paths = dfs_paths(graph, start, end)
        return {
            'paths': paths,
            'num_paths': len(paths),
            'shortest_path': min(paths, key=len) if paths else None
        }

    @staticmethod
    def detect_cycle(graph: Dict[int, List[int]]) -> Dict[str, Any]:
        """
        Detecta ciclos en un grafo dirigido usando DFS.

        Complejidad: O(V + E)

        Args:
            graph: Grafo representado como diccionario de adyacencia

        Returns:
            Dict indicando si existe ciclo
        """
        has_cycle = detect_cycle_dfs(graph)
        return {
            'has_cycle': has_cycle,
            'cycle_detected': has_cycle,
            'is_acyclic': not has_cycle
        }

    @staticmethod
    def topological_sort(graph: Dict[int, List[int]]) -> Dict[str, Any]:
        """
        Ordenamiento topológico de un grafo dirigido acíclico (DAG).

        Complejidad: O(V + E)

        Args:
            graph: Grafo dirigido acíclico

        Returns:
            Dict con orden topológico o error si hay ciclo
        """
        result = topological_sort_dfs(graph)
        if result is None:
            return {
                'success': False,
                'error': 'El grafo contiene ciclos (no es un DAG)',
                'order': None
            }
        return {
            'success': True,
            'order': result,
            'num_nodes': len(result)
        }

    # ==================== Dijkstra Algorithms ====================

    @staticmethod
    def dijkstra_shortest_paths(graph: Dict[int, List[Tuple[int, float]]], start: int) -> Dict[str, Any]:
        """
        Encuentra los caminos más cortos desde un nodo inicial usando Dijkstra.

        Complejidad: O((V + E) log V) con heap

        Args:
            graph: Grafo con pesos representado como {nodo: [(vecino, peso), ...]}
            start: Nodo inicial

        Returns:
            Dict con distancias y padres de todos los nodos alcanzables
        """
        result = dijkstra(graph, start)
        return {
            'start_node': start,
            'distances': result['distances'],
            'parents': result['parents'],
            'num_reachable': len(result['distances']),
            'algorithm': 'Dijkstra'
        }

    @staticmethod
    def dijkstra_path(graph: Dict[int, List[Tuple[int, float]]], start: int, end: int) -> Dict[str, Any]:
        """
        Encuentra el camino más corto entre dos nodos específicos usando Dijkstra.

        Complejidad: O((V + E) log V) con heap

        Args:
            graph: Grafo con pesos
            start: Nodo inicial
            end: Nodo final

        Returns:
            Dict con camino y distancia, o información de no alcanzable
        """
        result = dijkstra_path(graph, start, end)
        if result is None:
            return {
                'found': False,
                'path': None,
                'distance': None,
                'error': f'No existe camino desde {start} a {end}'
            }
        return {
            'found': True,
            'path': result['path'],
            'distance': result['distance'],
            'all_distances': result['all_distances']
        }

    @staticmethod
    def dijkstra_all_paths_from(graph: Dict[int, List[Tuple[int, float]]], start: int) -> Dict[str, Any]:
        """
        Encuentra todos los caminos más cortos desde un nodo inicial usando Dijkstra.

        Complejidad: O((V + E) log V) con heap

        Args:
            graph: Grafo con pesos
            start: Nodo inicial

        Returns:
            Dict con todos los caminos más cortos desde el nodo inicial
        """
        paths = dijkstra_all_paths(graph, start)
        return {
            'start_node': start,
            'paths': paths,
            'num_reachable': len(paths),
            'algorithm': 'Dijkstra All Paths'
        }

    # ==================== Bellman-Ford Algorithms ====================

    @staticmethod
    def bellman_ford_shortest_paths(graph: Dict[int, List[Tuple[int, float]]], start: int) -> Dict[str, Any]:
        """
        Encuentra los caminos más cortos usando Bellman-Ford.

        Funciona con pesos negativos pero detecta ciclos negativos.

        Complejidad: O(V * E)

        Args:
            graph: Grafo con pesos (puede tener pesos negativos)
            start: Nodo inicial

        Returns:
            Dict con distancias, padres, y detección de ciclos negativos
        """
        result = bellman_ford(graph, start)
        return {
            'start_node': start,
            'distances': result['distances'],
            'parents': result['parents'],
            'has_negative_cycle': result['has_negative_cycle'],
            'algorithm': 'Bellman-Ford'
        }

    @staticmethod
    def bellman_ford_path(graph: Dict[int, List[Tuple[int, float]]], start: int, end: int) -> Dict[str, Any]:
        """
        Encuentra el camino más corto entre dos nodos usando Bellman-Ford.

        Complejidad: O(V * E)

        Args:
            graph: Grafo con pesos
            start: Nodo inicial
            end: Nodo final

        Returns:
            Dict con camino y distancia
        """
        result = bellman_ford_path(graph, start, end)
        if result is None:
            return {
                'found': False,
                'error': f'No existe camino desde {start} a {end}'
            }
        return {
            'found': True,
            'path': result['path'],
            'distance': result['distance']
        }

    # ==================== Floyd-Warshall Algorithms ====================

    @staticmethod
    def floyd_warshall_all_pairs(graph: Dict[int, List[Tuple[int, float]]]) -> Dict[str, Any]:
        """
        Encuentra los caminos más cortos entre todos los pares de nodos.

        Complejidad: O(V³)

        Args:
            graph: Grafo con pesos

        Returns:
            Dict con matriz de distancias y matriz de caminos
        """
        result = floyd_warshall(graph)
        return {
            'distances': result['distances'],
            'paths': result.get('paths', {}),
            'algorithm': 'Floyd-Warshall',
            'num_nodes': len(result['distances']) if result['distances'] else 0
        }

    @staticmethod
    def floyd_warshall_path(graph: Dict[int, List[Tuple[int, float]]], start: int, end: int) -> Dict[str, Any]:
        """
        Encuentra el camino más corto entre dos nodos usando Floyd-Warshall.

        Complejidad: O(V³) para calcular todas las distancias

        Args:
            graph: Grafo con pesos
            start: Nodo inicial
            end: Nodo final

        Returns:
            Dict con camino y distancia
        """
        result = floyd_warshall_with_paths(graph, start, end)
        if result is None:
            return {
                'found': False,
                'error': f'No existe camino desde {start} a {end}'
            }
        return {
            'found': True,
            'path': result['path'],
            'distance': result['distance']
        }

    # ==================== MST Algorithms ====================

    @staticmethod
    def kruskal_mst(edges: List[Tuple[int, int, float]], num_vertices: int) -> Dict[str, Any]:
        """
        Encuentra el Árbol de Expansión Mínima usando Kruskal.

        Complejidad: O(E log E)

        Args:
            edges: Lista de aristas como (u, v, peso)
            num_vertices: Número de vértices

        Returns:
            Dict con aristas del MST y peso total
        """
        result = kruskal(edges, num_vertices)
        return {
            **result,
            'algorithm': 'Kruskal',
            'is_minimum_spanning_tree': result['is_connected']
        }

    @staticmethod
    def kruskal_mst_from_graph(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int) -> Dict[str, Any]:
        """
        Encuentra el MST desde una representación de grafo usando Kruskal.

        Complejidad: O(E log E)

        Args:
            graph: Grafo representado como {nodo: [(vecino, peso), ...]}
            num_vertices: Número de vértices

        Returns:
            Dict con información del MST
        """
        result = kruskal_from_graph(graph, num_vertices)
        return {
            **result,
            'algorithm': 'Kruskal'
        }

    @staticmethod
    def prim_mst(edges: List[Tuple[int, int, float]], num_vertices: int, start: int = 0) -> Dict[str, Any]:
        """
        Encuentra el Árbol de Expansión Mínima usando Prim.

        Complejidad: O(E log V) con heap

        Args:
            edges: Lista de aristas como (u, v, peso)
            num_vertices: Número de vértices
            start: Nodo inicial

        Returns:
            Dict con aristas del MST y peso total
        """
        result = prim(edges, num_vertices, start)
        return {
            **result,
            'algorithm': 'Prim',
            'start_node': start
        }

    @staticmethod
    def prim_mst_from_graph(graph: Dict[int, List[Tuple[int, float]]], num_vertices: int, start: int = 0) -> Dict[str, Any]:
        """
        Encuentra el MST desde una representación de grafo usando Prim.

        Complejidad: O(E log V) con heap

        Args:
            graph: Grafo representado como {nodo: [(vecino, peso), ...]}
            num_vertices: Número de vértices
            start: Nodo inicial

        Returns:
            Dict con información del MST
        """
        result = prim(graph, num_vertices, start)
        return {
            **result,
            'algorithm': 'Prim'
        }

    # ==================== Dynamic Programming Algorithms ====================

    @staticmethod
    def knapsack_01_problem(weights: List[int], values: List[int], capacity: int) -> Dict[str, Any]:
        """
        Resuelve el problema de la mochila 0/1 usando programación dinámica.

        Complejidad: O(n * W)

        Args:
            weights: Lista de pesos de los items
            values: Lista de valores de los items
            capacity: Capacidad de la mochila

        Returns:
            Dict con valor máximo e items seleccionados
        """
        result = knapsack_01(weights, values, capacity)
        return {
            **result,
            'algorithm': '0/1 Knapsack',
            'problem_size': len(weights),
            'capacity': capacity
        }

    @staticmethod
    def knapsack_unbounded_problem(weights: List[int], values: List[int], capacity: int) -> Dict[str, Any]:
        """
        Resuelve el problema de la mochila sin límite (unbounded knapsack).

        Complejidad: O(n * W)

        Args:
            weights: Lista de pesos de los items
            values: Lista de valores de los items
            capacity: Capacidad de la mochila

        Returns:
            Dict con valor máximo
        """
        result = knapsack_unbounded(weights, values, capacity)
        return {
            **result,
            'algorithm': 'Unbounded Knapsack',
            'problem_size': len(weights)
        }

    @staticmethod
    def knapsack_fractional_problem(weights: List[float], values: List[float], capacity: float) -> Dict[str, Any]:
        """
        Resuelve el problema de la mochila fraccionaria usando greedy.

        Complejidad: O(n log n)

        Args:
            weights: Lista de pesos
            values: Lista de valores
            capacity: Capacidad de la mochila

        Returns:
            Dict con valor máximo y fracciones de items
        """
        result = knapsack_fractional(weights, values, capacity)
        return {
            **result,
            'algorithm': 'Fractional Knapsack',
            'problem_size': len(weights)
        }

    @staticmethod
    def subset_sum_problem(numbers: List[int], target: int) -> Dict[str, Any]:
        """
        Resuelve el problema de suma de subconjunto (Subset Sum).

        Complejidad: O(n * target)

        Args:
            numbers: Lista de números
            target: Suma objetivo

        Returns:
            Dict indicando si es posible y el subconjunto
        """
        result = subset_sum(numbers, target)
        return {
            **result,
            'algorithm': 'Subset Sum',
            'target': target,
            'problem_size': len(numbers)
        }

    # ==================== Comparison and Analysis Methods ====================

    @staticmethod
    def compare_shortest_path_algorithms(
        graph: Dict[int, List[Tuple[int, float]]],
        start: int,
        end: int
    ) -> Dict[str, Any]:
        """
        Compara el resultado de diferentes algoritmos de camino más corto.

        Args:
            graph: Grafo con pesos
            start: Nodo inicial
            end: Nodo final

        Returns:
            Dict con resultados de Dijkstra, Bellman-Ford y Floyd-Warshall
        """
        return {
            'dijkstra': AlgorithmsService.dijkstra_path(graph, start, end),
            'bellman_ford': AlgorithmsService.bellman_ford_path(graph, start, end),
            'floyd_warshall': AlgorithmsService.floyd_warshall_path(graph, start, end),
            'comparison': 'Todos los algoritmos deberían dar el mismo resultado'
        }

    @staticmethod
    def get_algorithm_complexity_info() -> Dict[str, Dict[str, str]]:
        """
        Proporciona información sobre la complejidad de los algoritmos.

        Returns:
            Dict con complejidad temporal y espacial de cada algoritmo
        """
        return {
            'bfs': {'time': 'O(V + E)', 'space': 'O(V)'},
            'dfs': {'time': 'O(V + E)', 'space': 'O(V)'},
            'dijkstra': {'time': 'O((V + E) log V)', 'space': 'O(V)'},
            'bellman_ford': {'time': 'O(V * E)', 'space': 'O(V)'},
            'floyd_warshall': {'time': 'O(V³)', 'space': 'O(V²)'},
            'kruskal_mst': {'time': 'O(E log E)', 'space': 'O(V + E)'},
            'prim_mst': {'time': 'O(E log V)', 'space': 'O(V)'},
            'knapsack_01': {'time': 'O(n * W)', 'space': 'O(n * W)'},
            'knapsack_unbounded': {'time': 'O(n * W)', 'space': 'O(W)'},
            'knapsack_fractional': {'time': 'O(n log n)', 'space': 'O(n)'},
            'subset_sum': {'time': 'O(n * target)', 'space': 'O(n * target)'}
        }


algorithms_service = AlgorithmsService()
