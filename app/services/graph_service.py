"""
Graph Service - Manejo de construcción, conversión y estadísticas de grafos
Solo se incluyen transacciones de tipo 'egreso' para el análisis de gastos.
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.utils.graph_builder import GraphBuilder


class GraphService:
    """Servicio para manejo de grafos financieros."""

    @staticmethod
    def _get_egreso_transactions(db: Session) -> List[Transaction]:
        """
        Obtiene solo las transacciones de tipo 'egreso' de la base de datos.
        Los ingresos se excluyen del análisis de grafos ya que no aportan
        valor para el análisis de patrones de gasto.

        Args:
            db: Sesión de base de datos

        Returns:
            Lista de transacciones de tipo egreso
        """
        return db.query(Transaction).filter(Transaction.tipo == 'egreso').all()

    @staticmethod
    def build_gt_from_db(db: Session) -> Dict[int, List[tuple]]:
        """
        Construye Grafo de Transacciones (GT) desde la base de datos.
        Solo incluye transacciones de tipo 'egreso'.
        """
        transactions = GraphService._get_egreso_transactions(db)
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_gt(transactions_list)

    @staticmethod
    def build_gc_from_db(db: Session) -> Dict[str, List[tuple]]:
        """
        Construye Grafo de Categorías (GC) desde la base de datos.
        Solo incluye transacciones de tipo 'egreso'.
        """
        transactions = GraphService._get_egreso_transactions(db)
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_gc(transactions_list)

    @staticmethod
    def build_guc_from_db(db: Session) -> Dict[str, List[tuple]]:
        """
        Construye Grafo Usuario-Categoría (GUC) desde la base de datos.
        Solo incluye transacciones de tipo 'egreso'.
        """
        transactions = GraphService._get_egreso_transactions(db)
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_guc(transactions_list)

    @staticmethod
    def build_temporal_graph_from_db(db: Session, time_window_days: int = 7) -> Dict[int, List[tuple]]:
        """
        Construye grafo temporal. Solo incluye transacciones de tipo 'egreso'.
        """
        transactions = GraphService._get_egreso_transactions(db)
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_temporal_graph(transactions_list, time_window_days)

    @staticmethod
    def build_weighted_category_graph_from_db(db: Session) -> Dict[str, List[tuple]]:
        """
        Construye grafo de categorías ponderado. Solo incluye transacciones de tipo 'egreso'.
        """
        transactions = GraphService._get_egreso_transactions(db)
        transactions_list = GraphService._transactions_to_dict_list(transactions)
        return GraphBuilder.build_weighted_category_graph(transactions_list)

    @staticmethod
    def _transactions_to_dict_list(transactions: List[Transaction]) -> List[Dict[str, Any]]:
        return [
            {
                'id': trans.id,
                'fecha': trans.fecha,
                'tipo': trans.tipo,
                'categoria': trans.categoria,
                'subcategoria': trans.subcategoria,
                'descripcion': trans.descripcion,
                'metodo_pago': trans.metodo_pago,
                'monto': abs(trans.monto),
                'usuario': trans.usuario
            }
            for trans in transactions
        ]

    @staticmethod
    def get_graph_statistics(graph: Dict[Any, List[tuple]]) -> Dict[str, Any]:
        return GraphBuilder.get_graph_stats(graph)

    @staticmethod
    def get_gt_statistics(db: Session) -> Dict[str, Any]:
        gt = GraphService.build_gt_from_db(db)
        stats = GraphService.get_graph_statistics(gt)
        stats['graph_type'] = 'GT'
        return stats

    @staticmethod
    def get_gc_statistics(db: Session) -> Dict[str, Any]:
        gc = GraphService.build_gc_from_db(db)
        stats = GraphService.get_graph_statistics(gc)
        stats['graph_type'] = 'GC'
        return stats

    @staticmethod
    def get_guc_statistics(db: Session) -> Dict[str, Any]:
        guc = GraphService.build_guc_from_db(db)
        stats = GraphService.get_graph_statistics(guc)
        stats['graph_type'] = 'GUC'
        return stats

    @staticmethod
    def compare_graph_types(db: Session) -> Dict[str, Any]:
        return {
            'gt': GraphService.get_gt_statistics(db),
            'gc': GraphService.get_gc_statistics(db),
            'guc': GraphService.get_guc_statistics(db)
        }

    @staticmethod
    def get_graph_summary(db: Session) -> Dict[str, Any]:
        all_transactions = db.query(Transaction).all()
        egresos = [t for t in all_transactions if t.tipo == 'egreso']
        ingresos = [t for t in all_transactions if t.tipo == 'ingreso']

        num_egresos = len(egresos)
        total_egresos = sum(abs(t.monto) for t in egresos) if egresos else 0
        total_ingresos = sum(abs(t.monto) for t in ingresos) if ingresos else 0

        usuarios = set(t.usuario for t in egresos)
        categorias = set(t.categoria for t in egresos)

        return {
            'num_transactions': len(all_transactions),
            'num_egresos': num_egresos,
            'num_ingresos': len(ingresos),
            'num_usuarios': len(usuarios),
            'num_categorias': len(categorias),
            'total_egresos': float(total_egresos),
            'total_ingresos': float(total_ingresos),
            'balance': float(total_ingresos - total_egresos),
            'avg_egreso': float(total_egresos / num_egresos) if num_egresos > 0 else 0,
            'graphs_available': {
                'gt': num_egresos > 1,
                'gc': len(categorias) > 1,
                'guc': len(usuarios) > 0 and len(categorias) > 0
            },
            'nota': 'Los grafos solo incluyen transacciones de tipo egreso'
        }


graph_service = GraphService()
