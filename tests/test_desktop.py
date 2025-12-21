"""
Tests for CellularMap Desktop Tool
"""
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest import mock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_desktop_import():
    """Test that the desktop tool can be imported."""
    print("Testing desktop tool import...")
    try:
        import cellular_map_desktop
        from cellular_map_desktop import CellularMapDesktop
        print("✓ Desktop tool imports successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_desktop_initialization():
    """Test CellularMapDesktop class initialization."""
    print("\nTesting desktop initialization...")
    try:
        from cellular_map_desktop import CellularMapDesktop
        
        # Use a temporary directory for testing
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "CellularMapDesktop"
            desktop = CellularMapDesktop(home_dir=home_dir)
            
            # Verify directories were created
            assert desktop.home.exists(), "Home directory not created"
            assert desktop.exports.exists(), "Exports directory not created"
            assert desktop.logs.exists(), "Logs directory not created"
            assert desktop.data.exists(), "Data directory not created"
            
            # Verify configuration
            assert desktop.HIGH_GRAVITY_THRESHOLD == 0.8
            assert desktop.DISCOVERY_INTERVAL_HOURS == 4
            assert len(desktop.HIGH_IMPACT_GENES) == 5
            
            print("✓ Desktop initialization successful")
            return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False


def test_export_breakthroughs():
    """Test HTML report generation."""
    print("\nTesting export breakthroughs...")
    try:
        from cellular_map_desktop import CellularMapDesktop
        
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "CellularMapDesktop"
            desktop = CellularMapDesktop(home_dir=home_dir)
            
            # Generate a test report
            timestamp = "20251221_120000"
            html_path = desktop.export_breakthroughs(timestamp)
            
            # Verify HTML was created
            assert html_path.exists(), "HTML report not created"
            
            # Verify HTML content
            with open(html_path, "r") as f:
                content = f.read()
            
            assert "CellularMap Desktop" in content
            assert "Big dogs eat first" in content
            assert timestamp in content
            
            print("✓ Export breakthroughs successful")
            return True
    except Exception as e:
        print(f"✗ Export breakthroughs failed: {e}")
        return False


def test_api_base_url():
    """Test API base URL generation."""
    print("\nTesting API URL generation...")
    try:
        from cellular_map_desktop import CellularMapDesktop
        
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "CellularMapDesktop"
            desktop = CellularMapDesktop(home_dir=home_dir)
            
            url = desktop._get_api_base_url()
            assert url == "http://127.0.0.1:8000/api/v1"
            
            print("✓ API URL generation successful")
            return True
    except Exception as e:
        print(f"✗ API URL generation failed: {e}")
        return False


def test_cleanup():
    """Test cleanup functionality."""
    print("\nTesting cleanup...")
    try:
        from cellular_map_desktop import CellularMapDesktop
        
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "CellularMapDesktop"
            desktop = CellularMapDesktop(home_dir=home_dir)
            
            # Mock a process
            mock_proc = mock.Mock()
            mock_proc.poll.return_value = None  # Process is running
            mock_proc.wait.return_value = 0
            desktop.processes.append(("test", mock_proc))
            
            # Run cleanup
            desktop.cleanup()
            
            # Verify process was terminated
            mock_proc.terminate.assert_called_once()
            assert desktop._shutdown_requested is True
            
            print("✓ Cleanup successful")
            return True
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
        return False


def test_interruptible_sleep():
    """Test interruptible sleep functionality."""
    print("\nTesting interruptible sleep...")
    try:
        from cellular_map_desktop import CellularMapDesktop
        import time
        
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "CellularMapDesktop"
            desktop = CellularMapDesktop(home_dir=home_dir)
            
            # Set shutdown flag immediately
            desktop._shutdown_requested = True
            
            # This should return almost immediately
            start = time.time()
            desktop._interruptible_sleep(100)
            elapsed = time.time() - start
            
            # Should have exited quickly (within 11 seconds due to interval check)
            assert elapsed < 15, f"Sleep took too long: {elapsed}s"
            
            print("✓ Interruptible sleep successful")
            return True
    except Exception as e:
        print(f"✗ Interruptible sleep failed: {e}")
        return False


def main():
    """Run all desktop tool tests."""
    print("=" * 60)
    print("CellularMap Desktop Tool Tests")
    print("=" * 60)
    
    tests = [
        test_desktop_import,
        test_desktop_initialization,
        test_export_breakthroughs,
        test_api_base_url,
        test_cleanup,
        test_interruptible_sleep,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All desktop tool tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
