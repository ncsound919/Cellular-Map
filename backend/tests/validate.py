"""
Quick validation script for NetworkCellularMap v2.0 Backend
Tests basic functionality without requiring external dependencies
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from app.core.config import settings
        from app.models.schemas import (
            CellAgnosticNode, PanCellularEdge, CodexScores,
            DiagnosisRequest, DiagnosisResponse
        )
        from app.services.network import UniversalInteractomeService
        from app.services.ai_scientist import CausalDiscoveryService
        from app.services.codex import CodexMetricsService
        from app.services.repair import NetworkRepairEngine
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_schemas():
    """Test schema creation"""
    print("\nTesting schemas...")
    try:
        from app.models.schemas import (
            GenomePosition, CellAgnosticNode, PanCellularEdge,
            CodexScores, NetworkRole, MutationStatus
        )
        
        # Test GenomePosition
        pos = GenomePosition(chr="17", pos=7577548, ref="C", alt="T")
        
        # Test CellAgnosticNode
        node = CellAgnosticNode(
            universal_id="TP53",
            genome_position=pos,
            network_role=NetworkRole.HUB,
            mutation_status=MutationStatus.WT
        )
        
        # Test CodexScores
        scores = CodexScores(trueness=0.85, flow=0.90, gravity=0.88)
        
        print("✓ All schemas validated")
        return True
    except Exception as e:
        print(f"✗ Schema validation failed: {e}")
        return False


def test_services():
    """Test service initialization"""
    print("\nTesting services...")
    try:
        from app.services.network import UniversalInteractomeService
        from app.services.ai_scientist import CausalDiscoveryService
        from app.services.codex import CodexMetricsService, GamificationService
        from app.services.repair import NetworkRepairEngine
        
        # Initialize services
        network = UniversalInteractomeService()
        causal = CausalDiscoveryService()
        codex = CodexMetricsService()
        gamification = GamificationService()
        repair = NetworkRepairEngine()
        
        print("✓ All services initialized")
        return True
    except Exception as e:
        print(f"✗ Service initialization failed: {e}")
        return False


def test_codex_metrics():
    """Test Codex metrics calculations"""
    print("\nTesting Codex metrics...")
    try:
        from app.services.codex import CodexMetricsService
        
        codex = CodexMetricsService()
        
        # Test trueness
        trueness = codex.calculate_trueness("ATCG", "ATCG", 100)
        assert trueness == 1.0, f"Expected trueness=1.0, got {trueness}"
        
        # Test flow
        flow = codex.calculate_flow("AAV9_multitropic")
        assert flow == 0.95, f"Expected flow=0.95, got {flow}"
        
        # Test gravity
        gravity = codex.calculate_gravity(100, 0.9)
        assert gravity > 0, f"Expected gravity>0, got {gravity}"
        
        print("✓ Codex metrics calculations correct")
        return True
    except Exception as e:
        print(f"✗ Codex metrics test failed: {e}")
        return False


def test_crispr_design():
    """Test CRISPR design functionality"""
    print("\nTesting CRISPR design...")
    try:
        from app.services.repair import CrisprDesignService
        
        crispr = CrisprDesignService()
        
        # Test gRNA design
        grna = crispr.design_universal_grna("ATCGATCGATCGATCGATCGAAA", "TP53")
        assert len(grna) == 20, f"Expected gRNA length=20, got {len(grna)}"
        
        # Test HDR template
        hdr = crispr.generate_hdr_template("ATCGATCG")
        assert "HDR_TEMPLATE" in hdr, "HDR template not generated correctly"
        
        print("✓ CRISPR design working correctly")
        return True
    except Exception as e:
        print(f"✗ CRISPR design test failed: {e}")
        return False


def test_network_analysis():
    """Test network analysis"""
    print("\nTesting network analysis...")
    try:
        from app.services.network import UniversalInteractomeService
        from app.models.schemas import CellAgnosticNode, NetworkRole, MutationStatus
        
        network = UniversalInteractomeService()
        
        # Add some test nodes
        nodes = [
            CellAgnosticNode(
                universal_id=f"GENE_{i}",
                network_role=NetworkRole.HUB if i < 3 else NetworkRole.LEAF,
                mutation_status=MutationStatus.WT
            )
            for i in range(10)
        ]
        
        network.populate_nodes(nodes)
        
        # Check graph
        assert len(network.graph.nodes()) == 10, f"Expected 10 nodes, got {len(network.graph.nodes())}"
        
        print("✓ Network analysis working correctly")
        return True
    except Exception as e:
        print(f"✗ Network analysis test failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("NetworkCellularMap v2.0 Backend Validation")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_schemas,
        test_services,
        test_codex_metrics,
        test_crispr_design,
        test_network_analysis,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All validation tests passed! Backend is ready.")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
