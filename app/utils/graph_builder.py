"""
Graph Builder - Construcción de diferentes tipos de grafos desde transacciones
GT: Grafo de Transacciones
GC: Grafo de Categorías
GUC: Grafo de Usuario-Categoría
"""
from typing import List, Dict, Tuple
from datetime import date
from collections import defaultdict


class GraphBuilder:
    """Constructor de grafos a partir de transacciones financieras."""

    @staticmethod
    def build_gt(transactions: List[Dict]) -> Dict[int, List[Tuple[int, float]]]:
        """
        Construye Grafo de Transacciones (GT).
        Conecta transacciones secuenciales del mismo usuario.

        Args:
            transactions: Lista de transacciones

        Returns:
            Grafo dirigido con pesos (monto de transacción)
        """
        graph = defaultdict(list)

        # Ordenar por usuario y fecha
        sorted_trans = sorted(transactions, key=lambda x: (x.get('usuario', ''), x.get('fecha', date.min)))

        # Agrupar por usuario
        user_trans = defaultdict(list)
        for trans in sorted_trans:
            user_trans[trans.get('usuario', '')].append(trans)

        # Crear aristas entre transacciones consecutivas
        for usuario, trans_list in user_trans.items():
            for i in range(len(trans_list) - 1):
                current_id = trans_list[i].get('id', i)
                next_id = trans_list[i + 1].get('id', i + 1)
                weight = abs(trans_list[i + 1].get('monto', 0))

                graph[current_id].append((next_id, weight))

        return dict(graph)

    @staticmethod
    def build_gc(transactions: List[Dict]) -> Dict[str, List[Tuple[str, float]]]:
        """
        Construye Grafo de Categorías (GC).
        Conecta categorías basado en patrones de gasto.

        Args:
            transactions: Lista de transacciones

        Returns:
            Grafo no dirigido con pesos (frecuencia y monto)
        """
        graph = defaultdict(list)
        category_pairs = defaultdict(lambda: {'count': 0, 'total_amount': 0})

        # Ordenar por usuario y fecha
        sorted_trans = sorted(transactions, key=lambda x: (x.get('usuario', ''), x.get('fecha', date.min)))

        # Agrupar por usuario
        user_trans = defaultdict(list)
        for trans in sorted_trans:
            user_trans[trans.get('usuario', '')].append(trans)

        # Encontrar transiciones entre categorías
        for usuario, trans_list in user_trans.items():
            for i in range(len(trans_list) - 1):
                cat1 = trans_list[i].get('categoria', 'Unknown')
                cat2 = trans_list[i + 1].get('categoria', 'Unknown')

                if cat1 != cat2:
                    pair = tuple(sorted([cat1, cat2]))
                    category_pairs[pair]['count'] += 1
                    category_pairs[pair]['total_amount'] += trans_list[i + 1].get('monto', 0)

        # Construir grafo
        added_edges = set()
        for (cat1, cat2), data in category_pairs.items():
            weight = data['total_amount'] / data['count']  # Promedio

            if (cat1, cat2) not in added_edges:
                graph[cat1].append((cat2, weight))
                graph[cat2].append((cat1, weight))
                added_edges.add((cat1, cat2))
                added_edges.add((cat2, cat1))

        return dict(graph)

    @staticmethod
    def build_guc(transactions: List[Dict]) -> Dict[str, List[Tuple[str, float]]]:
        """
        Construye Grafo Usuario-Categoría (GUC).
        Grafo bipartito entre usuarios y categorías.

        Args:
            transactions: Lista de transacciones

        Returns:
            Grafo bipartito con pesos (monto total gastado)
        """
        graph = defaultdict(list)
        user_category_amount = defaultdict(float)

        # Calcular monto total por usuario-categoría
        for trans in transactions:
            usuario = f"U:{trans.get('usuario', 'Unknown')}"
            categoria = f"C:{trans.get('categoria', 'Unknown')}"
            monto = trans.get('monto', 0)

            user_category_amount[(usuario, categoria)] += monto

        # Construir grafo bipartito
        added_edges = set()
        for (usuario, categoria), monto in user_category_amount.items():
            if (usuario, categoria) not in added_edges:
                graph[usuario].append((categoria, monto))
                graph[categoria].append((usuario, monto))
                added_edges.add((usuario, categoria))
                added_edges.add((categoria, usuario))

        return dict(graph)

    @staticmethod
    def build_temporal_graph(transactions: List[Dict], time_window_days: int = 7) -> Dict[int, List[Tuple[int, float]]]:
        """
        Construye grafo temporal basado en ventana de tiempo.

        Args:
            transactions: Lista de transacciones
            time_window_days: Ventana de tiempo en días

        Returns:
            Grafo con conexiones dentro de la ventana temporal
        """
        graph = defaultdict(list)

        sorted_trans = sorted(transactions, key=lambda x: x.get('fecha', date.min))

        for i, trans1 in enumerate(sorted_trans):
            for trans2 in sorted_trans[i + 1:]:
                fecha1 = trans1.get('fecha', date.min)
                fecha2 = trans2.get('fecha', date.min)

                if isinstance(fecha1, str):
                    from datetime import datetime
                    fecha1 = datetime.strptime(fecha1, '%Y-%m-%d').date()
                if isinstance(fecha2, str):
                    from datetime import datetime
                    fecha2 = datetime.strptime(fecha2, '%Y-%m-%d').date()

                days_diff = abs((fecha2 - fecha1).days)

                if days_diff <= time_window_days:
                    id1 = trans1.get('id', i)
                    id2 = trans2.get('id', i + 1)
                    weight = trans2.get('monto', 0)

                    graph[id1].append((id2, weight))
                else:
                    break  # Ya están ordenados, no hay más dentro de la ventana

        return dict(graph)

    @staticmethod
    def build_weighted_category_graph(transactions: List[Dict]) -> Dict[str, List[Tuple[str, float]]]:
        """
        Construye grafo de categorías con pesos basados en frecuencia de transición.

        Args:
            transactions: Lista de transacciones

        Returns:
            Grafo de categorías con pesos de frecuencia
        """
        graph = defaultdict(list)
        transitions = defaultdict(int)

        sorted_trans = sorted(transactions, key=lambda x: (x.get('usuario', ''), x.get('fecha', date.min)))

        user_trans = defaultdict(list)
        for trans in sorted_trans:
            user_trans[trans.get('usuario', '')].append(trans)

        # Contar transiciones
        for usuario, trans_list in user_trans.items():
            for i in range(len(trans_list) - 1):
                cat1 = trans_list[i].get('categoria', 'Unknown')
                cat2 = trans_list[i + 1].get('categoria', 'Unknown')

                if cat1 != cat2:
                    transitions[(cat1, cat2)] += 1

        # Construir grafo dirigido
        for (cat1, cat2), count in transitions.items():
            graph[cat1].append((cat2, float(count)))

        return dict(graph)

    @staticmethod
    def get_graph_stats(graph: Dict) -> Dict[str, any]:
        """
        Obtiene estadísticas del grafo.

        Args:
            graph: Grafo

        Returns:
            Dict con estadísticas
        """
        num_nodes = len(graph)
        num_edges = sum(len(neighbors) for neighbors in graph.values())

        weights = []
        for neighbors in graph.values():
            for neighbor, weight in neighbors:
                weights.append(weight)

        return {
            "num_nodes": num_nodes,
            "num_edges": num_edges,
            "avg_degree": num_edges / num_nodes if num_nodes > 0 else 0,
            "avg_weight": sum(weights) / len(weights) if weights else 0,
            "max_weight": max(weights) if weights else 0,
            "min_weight": min(weights) if weights else 0
        }
