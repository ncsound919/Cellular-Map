"""
Example usage of the composable toolchain for NetworkCellularMap v2.0

This example demonstrates how to use the three layers:
1. Spatial/Network Core (Scanpy + Squidpy + NetworkX)
2. Training/AI Layer (PyTorch + PyG + scvi-tools)
3. Federated/Global Adoption (FedLab + OpenFL)
"""

import numpy as np
from app.services.spatial_omics import SpatialOmicsService
from app.services.network import UniversalInteractomeService
from app.services.federated_learning import FederatedLearningService
from app.services.orchestration import (
    NetworkologyDAG,
    TapSpeakGenerator,
    BBTechMetrics
)


def example_spatial_omics():
    """Example: Using Scanpy + Squidpy for spatial analysis"""
    print("\n=== Spatial Omics Example ===\n")
    
    # Create service
    spatial = SpatialOmicsService()
    
    # Generate sample data (in practice, load from file)
    n_cells = 1000
    n_genes = 2000
    expression_matrix = np.random.negative_binomial(5, 0.3, size=(n_cells, n_genes))
    gene_names = [f"GENE_{i}" for i in range(n_genes)]
    cell_names = [f"CELL_{i}" for i in range(n_cells)]
    
    # Step 1: Preprocess expression data
    print("1. Preprocessing expression data with Scanpy...")
    result = spatial.preprocess_expression_data(
        expression_matrix=expression_matrix,
        gene_names=gene_names,
        cell_names=cell_names
    )
    print(f"   Preprocessed {result.get('n_cells')} cells, {result.get('n_genes')} genes")
    print(f"   Found {result.get('n_highly_variable')} highly variable genes")
    
    # Step 2: Compute embeddings (UMAP)
    print("\n2. Computing UMAP embeddings...")
    embedding_result = spatial.compute_embeddings(method="umap", n_neighbors=15)
    print(f"   Embedding shape: {embedding_result.get('shape')}")
    
    # Step 3: Clustering
    print("\n3. Performing Leiden clustering...")
    cluster_result = spatial.perform_clustering(resolution=1.0, algorithm="leiden")
    print(f"   Found {cluster_result.get('n_clusters')} clusters")
    
    # Step 4: Build spatial neighborhood graph
    print("\n4. Building spatial neighborhood graph with Squidpy...")
    spatial_coords = np.random.rand(n_cells, 2) * 100  # Mock spatial coordinates
    spatial_graph = spatial.build_spatial_neighborhood_graph(
        spatial_coords=spatial_coords,
        coord_type="generic",
        n_neighs=6
    )
    print(f"   Spatial graph: {spatial_graph.number_of_nodes()} nodes, "
          f"{spatial_graph.number_of_edges()} edges")
    
    # Step 5: Export for SpatialGCN
    print("\n5. Exporting for SpatialGCN training...")
    gcn_data = spatial.export_for_spatialgcn()
    print(f"   Status: {gcn_data.get('status')}")
    
    return spatial, spatial_graph


def example_federated_learning():
    """Example: Using FedLab for simulation and OpenFL for production"""
    print("\n=== Federated Learning Example ===\n")
    
    # Simulation mode with FedLab
    print("1. Simulating federation with FedLab...")
    fl_sim = FederatedLearningService(mode="simulation")
    
    simulation = fl_sim.simulate_federation(
        n_clients=100,
        data_distribution="non_iid",
        client_type="clinic"
    )
    print(f"   Simulated {simulation['n_clients']} clients")
    print(f"   Total samples: {simulation['total_samples']}")
    print(f"   Framework: {simulation['framework']}")
    
    # Simulate Overlay365 network
    print("\n2. Simulating Overlay365 network...")
    overlay = fl_sim.simulate_overlay365_network(
        n_citizens=365,
        n_clinics=100
    )
    print(f"   Citizens: {overlay['citizens']}")
    print(f"   Clinics: {overlay['clinics']}")
    print(f"   Total participants: {overlay['total_participants']}")
    
    # Production mode with OpenFL
    print("\n3. Setting up production federation with OpenFL...")
    fl_prod = FederatedLearningService(mode="production")
    
    production_config = fl_prod.setup_production_federation(
        collaborators=["Hospital_A", "Hospital_B", "Hospital_C"],
        aggregator_address="https://aggregator.networkology.org"
    )
    print(f"   Framework: {production_config['framework']}")
    print(f"   Collaborators: {production_config['n_collaborators']}")
    print(f"   Security: TLS={production_config['security']['tls_enabled']}")
    
    # Configure privacy
    print("\n4. Configuring privacy-preserving training...")
    privacy = fl_prod.configure_privacy_preserving_training(
        differential_privacy=True,
        epsilon=1.0,
        secure_aggregation=True
    )
    print(f"   Differential Privacy: epsilon={privacy['privacy_config']['differential_privacy']['epsilon']}")
    print(f"   Secure Aggregation: {privacy['privacy_config']['secure_aggregation']['enabled']}")
    print(f"   GDPR Compliant: {privacy['gdpr_compliant']}")
    print(f"   HIPAA Compatible: {privacy['hipaa_compatible']}")
    
    return fl_sim, fl_prod


def example_orchestration():
    """Example: Using NetworkologyDAG for pipeline orchestration"""
    print("\n=== Orchestration Example ===\n")
    
    # Use pre-configured DAG
    print("1. Running NetworkologyDAG (ingest → map → analyze → intervene)...")
    dag = NetworkologyDAG()
    results = dag.run(gene="TP53")
    
    print(f"   Pipeline: {results['pipeline']}")
    print(f"   Status: {results['status']}")
    print(f"   Execution order: {' → '.join(results['execution_order'])}")
    
    # TapSpeak example
    print("\n2. Generating TapSpeak hooks...")
    tapspeak = TapSpeakGenerator()
    
    terms = ["hub", "scale_free", "Achilles_heel"]
    for term in terms:
        hook = tapspeak.generate_hook(term)
        print(f"   {term}: '{hook}'")
    
    # BBTech metrics
    print("\n3. Calculating BBTech metrics...")
    metrics = BBTechMetrics()
    
    trueness = metrics.calculate_trueness(restored_edges=80, total_disrupted_edges=100)
    flow = metrics.calculate_flow(delivered_molecules=950, target_molecules=1000)
    gravity = metrics.calculate_gravity(hub_degree=50, hub_betweenness=0.35)
    
    print(f"   Trueness: {trueness:.2f}")
    print(f"   Flow: {flow:.2f}")
    print(f"   Gravity: {gravity:.2f}")
    
    return results


def example_integration():
    """Example: Full integration of all three layers"""
    print("\n=== Full Integration Example ===\n")
    
    # Layer 1: Spatial/Network Core
    print("LAYER 1: Spatial/Network Core")
    spatial, spatial_graph = example_spatial_omics()
    
    # Create molecular network
    network = UniversalInteractomeService()
    # In practice, this would be populated from database
    network.graph.add_nodes_from([f"GENE_{i}" for i in range(100)])
    
    # Integrate spatial and molecular networks
    print("\n   Integrating spatial and molecular networks...")
    integrated_graph, metadata = spatial.integrate_with_network_map(
        spatial_graph=spatial_graph,
        gene_network=network.graph
    )
    print(f"   Integrated graph: {metadata['total_nodes']} nodes, "
          f"{metadata['total_edges']} edges")
    
    # Layer 2: Training/AI (export for PyTorch Geometric)
    print("\nLAYER 2: Training/AI")
    print("   Exporting data for SpatialGCN training...")
    gcn_data = spatial.export_for_spatialgcn()
    print(f"   Ready for PyTorch Geometric: {gcn_data.get('status')}")
    
    # Layer 3: Federated/Global Adoption
    print("\nLAYER 3: Federated/Global Adoption")
    fl_service = FederatedLearningService(mode="simulation")
    
    # Wrap model for federation
    print("   Wrapping SpatialGCN for federated training...")
    fed_model = fl_service.wrap_pytorch_model_for_federation(
        model_class="SpatialGCN",
        model_params={"hidden_channels": 64, "num_layers": 3}
    )
    print(f"   Model wrapped: {fed_model['ready_for_training']}")
    
    # Orchestration
    print("\nORCHESTRATION:")
    print("   Using NetworkologyDAG for complete workflow...")
    dag_results = example_orchestration()
    
    print("\n=== Integration Complete ===")
    print("\nThe composable toolchain successfully integrates:")
    print("  ✓ Scanpy + Squidpy (spatial omics)")
    print("  ✓ NetworkX (network analysis)")
    print("  ✓ PyTorch + PyG (GNN training)")
    print("  ✓ FedLab + OpenFL (federated learning)")
    print("  ✓ NetworkologyDAG (orchestration)")
    print("  ✓ TapSpeak + BBTech (metrics & communication)")


def main():
    """Run all examples"""
    print("=" * 70)
    print("NetworkCellularMap v2.0 - Composable Toolchain Examples")
    print("=" * 70)
    
    # Run individual examples
    example_spatial_omics()
    example_federated_learning()
    example_orchestration()
    
    # Run full integration
    example_integration()
    
    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
