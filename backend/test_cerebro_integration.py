#!/usr/bin/env python3
"""
Test script for Cerebro integration with NetworkCellularMap v2.0
Validates startup, API endpoints, and core functionality
"""

import sys
import asyncio
import importlib.util


def test_cerebro_module():
    """Test Cerebro module can be loaded and initialized"""
    print("="*60)
    print("TEST 1: Cerebro Module Loading")
    print("="*60)
    
    try:
        # Load cerebro module
        spec = importlib.util.spec_from_file_location('cerebro', 'app/services/cerebro.py')
        cerebro_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerebro_module)
        print("✓ Cerebro module loaded successfully")
        
        async def test_init():
            # Test initialization
            cerebro = cerebro_module.CerebroCore({'name': 'TestUser', 'field': 'Biotech'})
            await cerebro.start()
            
            # Test personalization
            await cerebro.personalize()
            
            # Test query
            result = await cerebro.process_query({'text': 'Test query', 'type': 'text'})
            assert result['status'] == 'success', "Query processing failed"
            
            # Test status
            status = cerebro.get_status()
            assert status['initialized'] == True, "Not initialized"
            
            print("✓ Cerebro initialization successful")
            print("✓ Personalization successful")
            print("✓ Query processing successful")
            print("✓ Status check successful")
            
        asyncio.run(test_init())
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_schemas():
    """Test Cerebro schemas are properly defined"""
    print("\n" + "="*60)
    print("TEST 2: Cerebro Schemas")
    print("="*60)
    
    try:
        from app.models.schemas import (
            CerebroUserProfile,
            CerebroQuery,
            CerebroResponse,
            CerebroReport,
            CerebroStatus
        )
        print("✓ All Cerebro schemas imported successfully")
        
        # Test schema validation
        profile = CerebroUserProfile(name="Test", field="Biotech")
        query = CerebroQuery(text="Test query")
        print("✓ Schema validation successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_router():
    """Test API router includes Cerebro endpoints"""
    print("\n" + "="*60)
    print("TEST 3: API Router Integration")
    print("="*60)
    
    try:
        from app.api.router import api_router
        
        # Check if cerebro routes are included
        routes = [route.path for route in api_router.routes]
        cerebro_routes = [r for r in routes if 'cerebro' in r]
        
        if cerebro_routes:
            print(f"✓ Found {len(cerebro_routes)} Cerebro routes:")
            for route in cerebro_routes:
                print(f"  - {route}")
        else:
            print("⚠ Warning: No Cerebro routes found in API router")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_services_export():
    """Test Cerebro is exported from services"""
    print("\n" + "="*60)
    print("TEST 4: Services Export")
    print("="*60)
    
    try:
        # Try importing without triggering other module imports
        with open('app/services/__init__.py', 'r') as f:
            content = f.read()
            
        if 'cerebro' in content.lower():
            print("✓ Cerebro found in services __init__.py")
        else:
            print("✗ Cerebro not found in services __init__.py")
            return False
            
        if 'CerebroCore' in content:
            print("✓ CerebroCore exported")
        if 'get_cerebro' in content:
            print("✓ get_cerebro exported")
        if 'initialize_cerebro' in content:
            print("✓ initialize_cerebro exported")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_main_integration():
    """Test main.py includes Cerebro initialization"""
    print("\n" + "="*60)
    print("TEST 5: Main.py Integration")
    print("="*60)
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
            
        checks = {
            'Cerebro import': 'initialize_cerebro' in content,
            'Cerebro startup': 'Cerebro.Networkology' in content,
            'Autonomous agent': 'Autonomous agent: Running' in content,
            'Cognitive profile': 'cognitive_profile' in content,
        }
        
        all_passed = True
        for check, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"{status} {check}: {passed}")
            all_passed = all_passed and passed
            
        return all_passed
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CEREBRO INTEGRATION TEST SUITE")
    print("="*60 + "\n")
    
    results = {
        "Cerebro Module": test_cerebro_module(),
        "Cerebro Schemas": test_schemas(),
        "API Router": test_api_router(),
        "Services Export": test_services_export(),
        "Main Integration": test_main_integration(),
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
