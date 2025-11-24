"""
Graph Service - Manejo de construcción, conversión y estadísticas de grafos
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.utils.graph_builder import GraphBuilder


class GraphService:
    """Servicio para manejo de grafos financieros."""

    @staticmethod
    def build_gt_from_db(db: Session) -> Dict[int, List[tuple]]:
        """
        Construye Grafo de Transacciones (GT) desde la base de datos.

        Conecta transacciones secuenciales del mismo usuario.

        Args:
            db: Sesión de base de datos

        Returns:
            Grafo dirigido con pesos (monto de transacción)
        """
        transactions = db.query(Transaction).all()
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_gt(transactions_list)

    @staticmethod
    def build_gc_from_db(db: Session) -> Dict[str, List[tuple]]:
        """
        Construye Grafo de Categorías (GC) desde la base de datos.

        Conecta categorías basado en patrones de gasto.

        Args:
            db: Sesión de base de datos

        Returns:
            Grafo no dirigido con pesos (frecuencia y monto)
        """
        transactions = db.query(Transaction).all()
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_gc(transactions_list)

    @staticmethod
    def build_guc_from_db(db: Session) -> Dict[str, List[tuple]]:
        """
        Construye Grafo Usuario-Categoría (GUC) desde la base de datos.

        Grafo bipartito entre usuarios y categorías.

        Args:
            db: Sesión de base de datos

        Returns:
            Grafo bipartito con pesos (monto total gastado)
        """
        transactions = db.query(Transaction).all()
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_guc(transactions_list)

    @staticmethod
    def build_temporal_graph_from_db(db: Session, time_window_days: int = 7) -> Dict[int, List[tuple]]:
        """
        Construye grafo temporal basado en ventana de tiempo desde la base de datos.

        Args:
            db: Sesión de base de datos
            time_window_days: Ventana de tiempo en días

        Returns:
            Grafo con conexiones dentro de la ventana temporal
        """
        transactions = db.query(Transaction).all()
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_temporal_graph(transactions_list, time_window_days)

    @staticmethod
    def build_weighted_category_graph_from_db(db: Session) -> Dict[str, List[tuple]]:
        """
        Construye grafo de categorías con pesos basados en frecuencia de transición.

        Args:
            db: Sesión de base de datos

        Returns:
            Grafo de categorías con pesos de frecuencia
        """
        transactions = db.query(Transaction).all()
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_weighted_category_graph(transactions_list)

    @staticmethod
    def _transactions_to_dict_list(transactions: List[Transaction]) -> List[Dict[str, Any]]:
        """
        Convierte objetos Transaction a diccionarios para el procesamiento de grafos.

        Args:
            transactions: Lista de objetos Transaction

        Returns:
            Lista de diccionarios con datos de transacciones
        """
        return [
            {
                'id': trans.id,
                'fecha': trans.fecha,
                'tipo': trans.tipo,
                'categoria': trans.categoria,
                'subcategoria': trans.subcategoria,
                'descripcion': trans.descripcion,
                'metodo_pago': trans.metodo_pago,
                'monto': abs(trans.monto),  # Usar valor absoluto
                'usuario': trans.usuario
            }
            for trans in transactions
        ]

    @staticmethod
    def get_graph_statistics(graph: Dict[Any, List[tuple]]) -> Dict[str, Any]:
        """
        Obtiene estadísticas de un grafo.

        Args:
            graph: Grafo representado como diccionario de adyacencia

        Returns:
            Dict con estadísticas del grafo
        """
        return GraphBuilder.get_graph_stats(graph)

    @staticmethod
    def get_gt_statistics(db: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas del Grafo de Transacciones.

        Args:
            db: Sesión de base de datos

        Returns:
            Dict con estadísticas del GT
        """
        gt = GraphService.build_gt_from_db(db)
        stats = GraphService.get_graph_statistics(gt)
        stats['graph_type'] = 'GT'
        return stats

    @staticmethod
    def get_gc_statistics(db: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas del Grafo de Categorías.

        Args:
            db: Sesión de base de datos

        Returns:
            Dict con estadísticas del GC
        """
        gc = GraphService.build_gc_from_db(db)
        stats = GraphService.get_graph_statistics(gc)
        stats['graph_type'] = 'GC'
        return stats

    @staticmethod
    def get_guc_statistics(db: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas del Grafo Usuario-Categoría.

        Args:
            db: Sesión de base de datos

        Returns:
            Dict con estadísticas del GUC
        """
        guc = GraphService.build_guc_from_db(db)
        stats = GraphService.get_graph_statistics(guc)
        stats['graph_type'] = 'GUC'
        return stats

    @staticmethod
    def compare_graph_types(db: Session) -> Dict[str, Any]:
        """
        Compara estadísticas de los tres tipos de grafos.

        Args:
            db: Sesión de base de datos

        Returns:
            Dict con estadísticas comparativas de todos los grafos
        """
        return {
            'gt': GraphService.get_gt_statistics(db),
            'gc': GraphService.get_gc_statistics(db),
            'guc': GraphService.get_guc_statistics(db)
        }

    @staticmethod
    def get_graph_summary(db: Session) -> Dict[str, Any]:
        """
        Obtiene un resumen general de los grafos disponibles.

        Args:
            db: Sesión de base de datos

        Returns:
            Dict con resumen de grafos y estadísticas clave
        """
        transactions = db.query(Transaction).all()
        num_transactions = len(transactions)

        # Estadísticas de transacciones
        total_amount = sum(t.monto for t in transactions) if transactions else 0

        # Usuarios y categorías únicos
        usuarios = set(t.usuario for t in transactions)
        categorias = set(t.categoria for t in transactions)

        return {
            'num_transactions': num_transactions,
            'num_usuarios': len(usuarios),
            'num_categorias': len(categorias),
            'total_amount': float(total_amount),
            'avg_transaction': float(total_amount / num_transactions) if num_transactions > 0 else 0,
            'graphs_available': {
                'gt': num_transactions > 1,
                'gc': len(categorias) > 1,
                'guc': len(usuarios) > 0 and len(categorias) > 0
            }
        }


graph_service = GraphService()
