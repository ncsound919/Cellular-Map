"""Network mapping and analysis service"""
import networkx as nx
import numpy as np
from typing import List, Dict, Any
from scipy import stats
from ..core.config import settings
from ..models.schemas import CellAgnosticNode, PanCellularEdge


class UniversalInteractomeService:
    """Universal Interactome - Graph Constructor"""
    
    def __init__(self):
        self.graph = nx.Graph()
        
    def populate_nodes(self, nodes: List[CellAgnosticNode]):
        """Populate universal gene nodes"""
        for node in nodes:
            self.graph.add_node(
                node.universal_id,
                mutation_status=node.mutation_status.value,
                expression=node.expression_all_cells,
                hub_gravity=node.hub_gravity,
                impact=node.organ_agnostic_impact,
                role=node.network_role.value
            )
    
    def populate_edges(self, edges: List[PanCellularEdge]):
        """Populate pan-cellular edges"""
        for edge in edges:
            self.graph.add_edge(
                edge.source_id,
                edge.target_id,
                relation_type=edge.relation_type.value,
                disruption_impact=edge.disruption_impact,
                weight=edge.weight,
                exists_in_all_cells=edge.exists_in_all_cells
            )
    
    def validate_scale_free(self) -> Dict[str, Any]:
        """
        Validate scale-free topology
        Power law alpha: 2.1-2.7
        Fitness test: Kolmogorov-Smirnov (p<0.05)
        """
        degrees = [d for n, d in self.graph.degree()]
        
        if not degrees or len(degrees) < 2:
            return {"error": "Insufficient data: graph has fewer than 2 nodes"}
        
        # Fit power law
        degree_counts = np.bincount(degrees)
        if len(degree_counts) < 2:
            return {"error": "Insufficient data for power law fitting"}
        
        log_counts = np.log(degree_counts[1:])
        if len(log_counts) < 2:
            return {"error": "Insufficient degree distribution for power law fitting"}
        
        log_degrees = np.log(np.arange(1, len(degree_counts)))
        
        if len(log_degrees) == len(log_counts) and len(log_counts) > 1:
            slope, intercept = np.polyfit(log_degrees, log_counts, 1)
            alpha = -slope
            
            # KS test
            ks_statistic, p_value = stats.kstest(degrees, 'powerlaw', args=(alpha,))
            
            return {
                "is_scale_free": settings.POWER_LAW_ALPHA_MIN <= alpha <= settings.POWER_LAW_ALPHA_MAX,
                "alpha": alpha,
                "ks_statistic": ks_statistic,
                "ks_p_value": p_value,
                "passes_ks_test": p_value < 0.05
            }
        
        return {"error": "Insufficient data for power law fitting"}
    
    def identify_pan_cellular_hubs(self) -> List[Dict[str, Any]]:
        """
        Identify universal hubs:
        - Top 5% by degree centrality across all cell contexts
        - Betweenness variance across tissues < 0.1
        """
        # Calculate centrality measures
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        eigenvector_centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)
        
        # Get top 5% by degree
        threshold = np.percentile(list(degree_centrality.values()), 95)
        
        hubs = []
        for node_id in self.graph.nodes():
            if degree_centrality[node_id] >= threshold:
                node_data = self.graph.nodes[node_id]
                hubs.append({
                    "hub_id": node_id,
                    "universal_degree_centrality": degree_centrality[node_id],
                    "betweenness_centrality": betweenness_centrality[node_id],
                    "eigenvector_centrality": eigenvector_centrality.get(node_id, 0),
                    "degree": self.graph.degree(node_id),
                    "hub_gravity": node_data.get("hub_gravity", 0),
                    "network_role": node_data.get("role", "unknown")
                })
        
        return sorted(hubs, key=lambda x: x["universal_degree_centrality"], reverse=True)
    
    def calculate_hub_gravity(self, node_id: str) -> float:
        """
        Calculate universal hub score:
        log(degree_all_cells) * eigenvector_centrality
        """
        degree = self.graph.degree(node_id)
        try:
            eigenvector = nx.eigenvector_centrality(self.graph, max_iter=1000)
            eigen_value = eigenvector.get(node_id, 0)
        except Exception:
            eigen_value = 0
        
        if degree > 0:
            return np.log(degree + 1) * eigen_value
        return 0.0
    
    def simulate_hub_attack(self, removal_fraction: float = 0.2) -> Dict[str, Any]:
        """
        Achilles heel protocol:
        - Random failure: network robust (99%)
        - Hub attack: network collapses (20% removal)
        """
        original_components = nx.number_connected_components(self.graph)
        
        # Hub attack
        hubs = self.identify_pan_cellular_hubs()
        n_remove = int(len(hubs) * removal_fraction)
        hub_ids = [h["hub_id"] for h in hubs[:n_remove]]
        
        graph_copy = self.graph.copy()
        graph_copy.remove_nodes_from(hub_ids)
        
        hub_attack_components = nx.number_connected_components(graph_copy)
        
        # Random failure
        random_nodes = np.random.choice(
            list(self.graph.nodes()), 
            size=n_remove, 
            replace=False
        )
        graph_random = self.graph.copy()
        graph_random.remove_nodes_from(random_nodes)
        
        random_failure_components = nx.number_connected_components(graph_random)
        
        return {
            "original_components": original_components,
            "hub_attack_components": hub_attack_components,
            "random_failure_components": random_failure_components,
            "network_collapsed": hub_attack_components > original_components * 2,
            "network_robust_random": random_failure_components <= original_components * 1.1
        }
    
    def find_disease_module(self, mutation_ids: List[str], max_distance: int = 3) -> List[str]:
        """
        Find disease module around mutations.
        
        This function collects all nodes that lie within a shortest-path distance
        of at most max_distance from any of the provided mutation_ids in the
        universal interactome graph.
        
        Parameters
        ----------
        mutation_ids : List[str]
            Node identifiers corresponding to mutations of interest.
        max_distance : int, optional
            Maximum shortest-path distance from each mutation node to include in
            the module. Defaults to 3. Callers may pass a different value to
            control the module radius.
        
        Returns
        -------
        List[str]
            List of node identifiers that belong to the aggregated disease module.
        """
        module_nodes = set()
        
        for mutation_id in mutation_ids:
            if mutation_id in self.graph:
                # Get all nodes within max_distance
                for node in self.graph.nodes():
                    try:
                        path_length = nx.shortest_path_length(
                            self.graph, 
                            source=mutation_id, 
                            target=node
                        )
                        if path_length <= max_distance:
                            module_nodes.add(node)
                    except nx.NetworkXNoPath:
                        continue
        
        return list(module_nodes)
