"""Spatial Omics Service - Scanpy + Squidpy integration for tissue geometry"""
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import networkx as nx


class SpatialOmicsService:
    """
    Lightweight spatial layer for single-cell spatial omics.
    Uses Scanpy for preprocessing and Squidpy for spatial graphs.
    """
    
    def __init__(self):
        """Initialize spatial omics service with lazy imports"""
        self.adata = None
        
    def preprocess_expression_data(
        self, 
        expression_matrix: np.ndarray,
        gene_names: List[str],
        cell_names: List[str]
    ) -> Dict[str, Any]:
        """
        Preprocess single-cell expression data using Scanpy.
        
        Parameters
        ----------
        expression_matrix : np.ndarray
            Cell x Gene expression matrix
        gene_names : List[str]
            Gene identifiers
        cell_names : List[str]
            Cell identifiers
            
        Returns
        -------
        Dict[str, Any]
            Preprocessed data with normalized counts, scaled data, and QC metrics
        """
        try:
            import scanpy as sc
            import anndata
            
            # Create AnnData object (efficient H5 backing)
            self.adata = anndata.AnnData(
                X=expression_matrix,
                obs={'cell_id': cell_names},
                var={'gene_name': gene_names}
            )
            
            # Quality control
            sc.pp.calculate_qc_metrics(self.adata, inplace=True)
            
            # Normalize and log-transform
            sc.pp.normalize_total(self.adata, target_sum=1e4)
            sc.pp.log1p(self.adata)
            
            # Identify highly variable genes
            sc.pp.highly_variable_genes(self.adata, n_top_genes=2000)
            
            # Scale data
            sc.pp.scale(self.adata, max_value=10)
            
            return {
                "status": "success",
                "n_cells": self.adata.n_obs,
                "n_genes": self.adata.n_vars,
                "n_highly_variable": sum(self.adata.var['highly_variable']),
                "preprocessed": True
            }
        except ImportError:
            return {
                "status": "error",
                "message": "Scanpy not installed. Install with: pip install scanpy"
            }
    
    def compute_embeddings(
        self,
        method: str = "umap",
        n_neighbors: int = 15,
        n_components: int = 2
    ) -> Dict[str, Any]:
        """
        Compute dimensionality reduction embeddings (UMAP/PHATE).
        
        Parameters
        ----------
        method : str
            Embedding method ('umap' or 'phate')
        n_neighbors : int
            Number of neighbors for graph construction
        n_components : int
            Number of embedding dimensions
            
        Returns
        -------
        Dict[str, Any]
            Embedding coordinates and metadata
        """
        if self.adata is None:
            return {"error": "No data loaded. Run preprocess_expression_data first."}
        
        try:
            import scanpy as sc
            
            # Compute PCA first
            sc.tl.pca(self.adata, svd_solver='arpack')
            
            # Compute neighbors
            sc.pp.neighbors(self.adata, n_neighbors=n_neighbors, n_pcs=40)
            
            # Compute embedding
            if method.lower() == "umap":
                sc.tl.umap(self.adata, n_components=n_components)
                embedding = self.adata.obsm['X_umap']
            elif method.lower() == "phate":
                # PHATE requires separate installation
                try:
                    import phate
                    phate_op = phate.PHATE(n_components=n_components, knn=n_neighbors)
                    embedding = phate_op.fit_transform(self.adata.X)
                    self.adata.obsm['X_phate'] = embedding
                except ImportError:
                    return {
                        "error": "PHATE not installed. Install with: pip install phate"
                    }
            else:
                return {"error": f"Unknown embedding method: {method}"}
            
            return {
                "status": "success",
                "method": method,
                "shape": embedding.shape,
                "n_components": n_components,
                "embedding_key": f"X_{method}"
            }
        except ImportError:
            return {
                "status": "error",
                "message": "Scanpy not installed. Install with: pip install scanpy"
            }
    
    def perform_clustering(
        self,
        resolution: float = 1.0,
        algorithm: str = "leiden"
    ) -> Dict[str, Any]:
        """
        Perform clustering on preprocessed data.
        
        Parameters
        ----------
        resolution : float
            Resolution parameter for clustering
        algorithm : str
            Clustering algorithm ('leiden' or 'louvain')
            
        Returns
        -------
        Dict[str, Any]
            Cluster assignments and statistics
        """
        if self.adata is None:
            return {"error": "No data loaded. Run preprocess_expression_data first."}
        
        try:
            import scanpy as sc
            
            # Run clustering
            if algorithm.lower() == "leiden":
                sc.tl.leiden(self.adata, resolution=resolution)
                cluster_key = 'leiden'
            elif algorithm.lower() == "louvain":
                sc.tl.louvain(self.adata, resolution=resolution)
                cluster_key = 'louvain'
            else:
                return {"error": f"Unknown clustering algorithm: {algorithm}"}
            
            clusters = self.adata.obs[cluster_key]
            
            return {
                "status": "success",
                "algorithm": algorithm,
                "n_clusters": len(clusters.unique()),
                "resolution": resolution,
                "cluster_sizes": clusters.value_counts().to_dict()
            }
        except ImportError:
            return {
                "status": "error",
                "message": "Scanpy not installed. Install with: pip install scanpy"
            }
    
    def build_spatial_neighborhood_graph(
        self,
        spatial_coords: np.ndarray,
        coord_type: str = "generic",
        n_neighs: int = 6,
        radius: Optional[float] = None
    ) -> nx.Graph:
        """
        Build spatial neighborhood graph using Squidpy.
        
        Parameters
        ----------
        spatial_coords : np.ndarray
            Spatial coordinates (n_cells x 2 or 3)
        coord_type : str
            Type of coordinates ('generic', 'grid', 'visium')
        n_neighs : int
            Number of neighbors for spatial graph
        radius : Optional[float]
            Radius for spatial graph (if None, uses n_neighs)
            
        Returns
        -------
        nx.Graph
            Spatial neighborhood graph for SpatialGCN
        """
        if self.adata is None:
            # Create minimal AnnData if not exists
            import anndata
            self.adata = anndata.AnnData(
                X=np.zeros((spatial_coords.shape[0], 1)),
                obsm={'spatial': spatial_coords}
            )
        else:
            self.adata.obsm['spatial'] = spatial_coords
        
        try:
            import squidpy as sq
            
            # Build spatial graph
            sq.gr.spatial_neighbors(
                self.adata,
                coord_type=coord_type,
                n_neighs=n_neighs,
                radius=radius,
                spatial_key='spatial'
            )
            
            # Extract graph as NetworkX
            adjacency = self.adata.obsp['spatial_connectivities']
            G = nx.from_scipy_sparse_array(adjacency)
            
            # Add spatial coordinates as node attributes
            for i, coords in enumerate(spatial_coords):
                G.nodes[i]['spatial_x'] = float(coords[0])
                G.nodes[i]['spatial_y'] = float(coords[1])
                if coords.shape[0] > 2:
                    G.nodes[i]['spatial_z'] = float(coords[2])
            
            return G
            
        except ImportError:
            # Fallback to basic spatial graph without Squidpy
            from scipy.spatial import distance_matrix
            
            G = nx.Graph()
            G.add_nodes_from(range(len(spatial_coords)))
            
            # Add spatial coordinates
            for i, coords in enumerate(spatial_coords):
                G.nodes[i]['spatial_x'] = float(coords[0])
                G.nodes[i]['spatial_y'] = float(coords[1])
                if coords.shape[0] > 2:
                    G.nodes[i]['spatial_z'] = float(coords[2])
            
            # Compute distances
            dist_matrix = distance_matrix(spatial_coords, spatial_coords)
            
            # Connect to k nearest neighbors
            for i in range(len(spatial_coords)):
                nearest = np.argsort(dist_matrix[i])[1:n_neighs+1]
                for j in nearest:
                    G.add_edge(i, j, weight=1.0/dist_matrix[i, j])
            
            return G
    
    def extract_image_features(
        self,
        image_path: str,
        spatial_coords: np.ndarray,
        features: List[str] = ["texture", "summary"]
    ) -> Dict[str, Any]:
        """
        Extract image features at spatial locations using Squidpy.
        
        Parameters
        ----------
        image_path : str
            Path to tissue image
        spatial_coords : np.ndarray
            Spatial coordinates for feature extraction
        features : List[str]
            Feature types to extract
            
        Returns
        -------
        Dict[str, Any]
            Extracted image features
        """
        try:
            import squidpy as sq
            
            if self.adata is None or 'spatial' not in self.adata.obsm:
                return {"error": "Spatial coordinates not set. Run build_spatial_neighborhood_graph first."}
            
            # This is a placeholder - actual implementation would load image
            # and extract features at specified locations
            
            return {
                "status": "success",
                "features": features,
                "n_locations": len(spatial_coords),
                "note": "Feature extraction placeholder - requires actual image data"
            }
            
        except ImportError:
            return {
                "status": "error",
                "message": "Squidpy not installed. Install with: pip install squidpy"
            }
    
    def integrate_with_network_map(
        self,
        spatial_graph: nx.Graph,
        gene_network: nx.Graph
    ) -> Tuple[nx.Graph, Dict[str, Any]]:
        """
        Integrate spatial tissue graph with gene interaction network.
        Creates a multi-layer network for SpatialGCN analysis.
        
        Parameters
        ----------
        spatial_graph : nx.Graph
            Spatial neighborhood graph from tissue
        gene_network : nx.Graph
            Gene interaction network
            
        Returns
        -------
        Tuple[nx.Graph, Dict[str, Any]]
            Integrated multi-layer graph and metadata
        """
        # Create multi-layer graph
        integrated = nx.Graph()
        
        # Add spatial layer (cell-cell interactions)
        for node, data in spatial_graph.nodes(data=True):
            integrated.add_node(f"cell_{node}", layer="spatial", **data)
        
        for u, v, data in spatial_graph.edges(data=True):
            integrated.add_edge(f"cell_{u}", f"cell_{v}", layer="spatial", **data)
        
        # Add molecular layer (gene-gene interactions)
        for node, data in gene_network.nodes(data=True):
            integrated.add_node(f"gene_{node}", layer="molecular", **data)
        
        for u, v, data in gene_network.edges(data=True):
            integrated.add_edge(f"gene_{u}", f"gene_{v}", layer="molecular", **data)
        
        # Add cross-layer edges (cell-gene expression)
        # This would be populated based on actual expression data
        
        metadata = {
            "spatial_nodes": spatial_graph.number_of_nodes(),
            "spatial_edges": spatial_graph.number_of_edges(),
            "molecular_nodes": gene_network.number_of_nodes(),
            "molecular_edges": gene_network.number_of_edges(),
            "total_nodes": integrated.number_of_nodes(),
            "total_edges": integrated.number_of_edges()
        }
        
        return integrated, metadata
    
    def export_for_spatialgcn(self) -> Dict[str, Any]:
        """
        Export preprocessed data in format ready for SpatialGCN training.
        
        Returns
        -------
        Dict[str, Any]
            Data formatted for PyTorch Geometric SpatialGCN
        """
        if self.adata is None:
            return {"error": "No data loaded. Run preprocess_expression_data first."}
        
        return {
            "status": "success",
            "expression_matrix": self.adata.X if hasattr(self.adata, 'X') else None,
            "spatial_graph": self.adata.obsp.get('spatial_connectivities'),
            "embeddings": self.adata.obsm if hasattr(self.adata, 'obsm') else {},
            "clusters": self.adata.obs if hasattr(self.adata, 'obs') else {},
            "highly_variable_genes": self.adata.var.get('highly_variable') if hasattr(self.adata, 'var') else None,
            "note": "Export ready for PyTorch Geometric DataLoader"
        }
