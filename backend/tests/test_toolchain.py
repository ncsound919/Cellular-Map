"""
Simple validation tests for the composable toolchain services
"""
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.spatial_omics import SpatialOmicsService
from app.services.federated_learning import FederatedLearningService
from app.services.orchestration import (
    NetworkologyPipeline,
    NetworkologyDAG,
    TapSpeakGenerator,
    BBTechMetrics
)


def test_spatial_omics_service():
    """Test SpatialOmicsService basic functionality"""
    print("\n=== Testing SpatialOmicsService ===")
    
    service = SpatialOmicsService()
    
    # Test 1: Basic initialization
    assert service.adata is None, "Initial adata should be None"
    print("✓ Service initialization")
    
    # Test 2: Build spatial graph (without Squidpy)
    spatial_coords = np.random.rand(100, 2) * 100
    graph = service.build_spatial_neighborhood_graph(
        spatial_coords=spatial_coords,
        n_neighs=6
    )
    
    assert graph.number_of_nodes() == 100, "Graph should have 100 nodes"
    assert graph.number_of_edges() > 0, "Graph should have edges"
    print(f"✓ Spatial graph construction: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    
    # Test 3: Integration with network map
    import networkx as nx
    gene_network = nx.Graph()
    gene_network.add_nodes_from([f"GENE_{i}" for i in range(50)])
    
    integrated, metadata = service.integrate_with_network_map(
        spatial_graph=graph,
        gene_network=gene_network
    )
    
    assert integrated.number_of_nodes() == 150, "Integrated graph should have 150 nodes"
    assert metadata['spatial_nodes'] == 100
    assert metadata['molecular_nodes'] == 50
    print(f"✓ Network integration: {metadata['total_nodes']} total nodes")
    
    print("✓ All SpatialOmicsService tests passed")
    return True


def test_federated_learning_service():
    """Test FederatedLearningService basic functionality"""
    print("\n=== Testing FederatedLearningService ===")
    
    # Test 1: Simulation mode
    fl_sim = FederatedLearningService(mode="simulation")
    assert fl_sim.mode == "simulation", "Mode should be simulation"
    print("✓ Simulation mode initialization")
    
    # Test 2: Simulate federation
    result = fl_sim.simulate_federation(n_clients=50, client_type="clinic")
    assert result['status'] == 'success', "Simulation should succeed"
    assert result['n_clients'] == 50, "Should have 50 clients"
    assert len(fl_sim.clients) == 50, "Service should store 50 clients"
    print(f"✓ Federation simulation: {result['n_clients']} clients, {result['total_samples']} samples")
    
    # Test 3: Overlay365 network
    overlay = fl_sim.simulate_overlay365_network(n_citizens=365, n_clinics=100)
    assert overlay['status'] == 'success', "Overlay simulation should succeed"
    assert overlay['citizens'] == 365
    assert overlay['clinics'] == 100
    print(f"✓ Overlay365 network: {overlay['total_participants']} participants")
    
    # Test 4: Production mode
    fl_prod = FederatedLearningService(mode="production")
    config = fl_prod.setup_production_federation(
        collaborators=["Hospital_A", "Hospital_B"],
        aggregator_address="https://test.example.com"
    )
    assert config['status'] == 'success', "Production setup should succeed"
    assert config['framework'] == 'OpenFL'
    print(f"✓ Production federation: {config['n_collaborators']} collaborators")
    
    # Test 5: Privacy configuration
    privacy = fl_prod.configure_privacy_preserving_training(
        differential_privacy=True,
        epsilon=1.0
    )
    assert privacy['status'] == 'success'
    assert privacy['gdpr_compliant'] == True
    assert privacy['hipaa_compatible'] == True
    print(f"✓ Privacy configuration: DP enabled, GDPR compliant")
    
    print("✓ All FederatedLearningService tests passed")
    return True


def test_orchestration_services():
    """Test orchestration utilities"""
    print("\n=== Testing Orchestration Services ===")
    
    # Test 1: NetworkologyPipeline
    pipeline = NetworkologyPipeline("TestPipeline")
    
    def stage1(inputs):
        return {"result": "stage1_output"}
    
    def stage2(inputs):
        return {"result": "stage2_output", "input_from_stage1": inputs.get("stage1")}
    
    pipeline.add_stage("stage1", stage1, dependencies=[])
    pipeline.add_stage("stage2", stage2, dependencies=["stage1"])
    
    results = pipeline.execute()
    assert results['status'] == 'completed', "Pipeline should complete"
    assert len(results['execution_order']) == 2, "Should execute 2 stages"
    assert results['execution_order'] == ['stage1', 'stage2'], "Correct execution order"
    print(f"✓ Pipeline execution: {' → '.join(results['execution_order'])}")
    
    # Test 2: NetworkologyDAG
    dag = NetworkologyDAG()
    dag_results = dag.run(gene="TP53")
    assert dag_results['status'] in ['completed', 'failed'], "DAG should execute"
    assert len(dag_results['execution_order']) == 4, "Should have 4 stages"
    print(f"✓ NetworkologyDAG: {' → '.join(dag_results['execution_order'])}")
    
    # Test 3: TapSpeakGenerator
    tapspeak = TapSpeakGenerator()
    hook = tapspeak.generate_hook("hub")
    assert hook == "network traffic controller", "Should return correct hook"
    print(f"✓ TapSpeak: 'hub' → '{hook}'")
    
    # Update lexicon
    tapspeak.update_lexicon("test_term", "test hook", "test explanation")
    assert "test_term" in tapspeak.lexicon
    print("✓ Lexicon update")
    
    # Test 4: BBTechMetrics
    metrics = BBTechMetrics()
    
    trueness = metrics.calculate_trueness(80, 100)
    assert trueness == 0.8, "Trueness calculation"
    
    flow = metrics.calculate_flow(950, 1000)
    assert flow == 0.95, "Flow calculation"
    
    gravity = metrics.calculate_gravity(50, 0.35)
    assert gravity > 0, "Gravity calculation"
    
    print(f"✓ BBTech Metrics: Trueness={trueness:.2f}, Flow={flow:.2f}, Gravity={gravity:.2f}")
    
    print("✓ All Orchestration tests passed")
    return True


def main():
    """Run all tests"""
    print("=" * 70)
    print("Composable Toolchain Validation Tests")
    print("=" * 70)
    
    try:
        # Run tests
        test_spatial_omics_service()
        test_federated_learning_service()
        test_orchestration_services()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
