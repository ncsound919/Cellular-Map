"""
Cerebro Usage Examples
Demonstrates autonomous agent, personalization, and copilot features

Run from backend directory: python -m examples.cerebro_usage
Or standalone with path fix (see main)
"""

import asyncio
import sys
import os

# Fix import path when run standalone
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.cerebro import CerebroCore, initialize_cerebro


async def example_1_basic_initialization():
    """Example 1: Basic Cerebro initialization and personalization"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Initialization")
    print("="*60 + "\n")
    
    # Create user profile
    user = {
        "name": "Dr. Smith",
        "field": "Biotech"
    }
    
    # Initialize Cerebro
    cerebro = await initialize_cerebro(user)
    
    # Check status
    status = cerebro.get_status()
    print(f"✓ User: {status['user']}")
    print(f"✓ Cognitive Profile: {status['cognitive_profile']}")
    print(f"✓ Agent Running: {status['agent_running']}")


async def example_2_query_processing():
    """Example 2: Process queries with copilot assistance"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Query Processing")
    print("="*60 + "\n")
    
    cerebro = CerebroCore({"name": "Researcher", "field": "Networkology"})
    await cerebro.start()
    await cerebro.personalize()
    
    # Example queries
    queries = [
        "Design CRISPR for pan-cellular obesity hubs",
        "Analyze MC4R network centrality",
        "Find Achilles heels in liver manifold"
    ]
    
    for query_text in queries:
        print(f"\nQuery: {query_text}")
        result = await cerebro.process_query({
            "text": query_text,
            "type": "text"
        })
        
        print(f"  TapSpeak: {result.get('tap_speak')}")
        print(f"  Status: {result.get('status')}")
        
        if result.get('copilot_thoughts', {}).get('suggestions'):
            print("  Copilot Suggestions:")
            for suggestion in result['copilot_thoughts']['suggestions']:
                print(f"    - {suggestion}")


async def example_3_nightly_report():
    """Example 3: Get autonomous agent's nightly discoveries"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Nightly Report")
    print("="*60 + "\n")
    
    cerebro = CerebroCore({"name": "Networkologist", "field": "Biotech"})
    await cerebro.start()
    
    # Get nightly report
    report = await cerebro.nightly_report()
    
    print(f"Report: {report['title']}\n")
    
    for section_name, items in report['sections'].items():
        if items:
            print(f"{section_name}:")
            for item in items:
                if isinstance(item, dict):
                    print(f"  - {item.get('description', item.get('type', str(item)))}")
                else:
                    print(f"  - {item}")
            print()


async def example_4_copilot_mode():
    """Example 4: Real-time copilot interaction"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Real-time Copilot Mode")
    print("="*60 + "\n")
    
    cerebro = CerebroCore({"name": "Lab Researcher", "field": "Systems Biology"})
    await cerebro.start()
    await cerebro.personalize()
    
    # Simulate real-time analysis
    observations = [
        "Looking at MC4R protein structure...",
        "Expression pattern shows pan-cellular distribution",
        "Mutation rate higher than expected in hub nodes"
    ]
    
    for observation in observations:
        print(f"\nYou: {observation}")
        
        # Get copilot thoughts
        thoughts = await cerebro.copilot.think_alongside({
            "text": observation,
            "type": "text"
        })
        
        if thoughts.get('has_immediate_value'):
            print("Copilot:")
            for suggestion in thoughts.get('suggestions', []):
                print(f"  💡 {suggestion}")


async def example_5_cognitive_profiles():
    """Example 5: Different cognitive profiles"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Cognitive Profiles")
    print("="*60 + "\n")
    
    # Different user profiles
    users = [
        {"name": "Explorer", "field": "Biotech"},
        {"name": "Hub Hunter", "field": "Network Medicine"},
        {"name": "Spatial Thinker", "field": "Systems Biology"}
    ]
    
    for user in users:
        cerebro = CerebroCore(user)
        await cerebro.personalize()
        
        profile = cerebro.cognitive_profile
        print(f"\nUser: {user['name']}")
        print(f"  Style: {profile['style']}")
        print(f"  Preferences:")
        for key, value in profile['preferences'].items():
            print(f"    - {key}: {value}")
        print(f"  Detected Patterns: {', '.join(profile['detected_patterns'])}")


async def example_6_memory_system():
    """Example 6: Memory and learning"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Memory System")
    print("="*60 + "\n")
    
    cerebro = CerebroCore({"name": "Researcher", "field": "Biotech"})
    await cerebro.start()
    
    # Record some events
    events = [
        {"type": "experiment", "description": "Tested MC4R CRISPR design"},
        {"type": "analysis", "description": "Found 3 new hubs in liver"},
        {"type": "discovery", "description": "Pan-cellular obesity pathway identified"}
    ]
    
    for event in events:
        await cerebro.memory.observe(event)
        print(f"✓ Recorded: {event['description']}")
    
    print(f"\nMemory size: {len(cerebro.memory.episodic_memory)} events")
    
    # Recall memories
    memories = await cerebro.memory.recall(
        "obesity pathway",
        context=await cerebro.get_full_context()
    )
    
    print(f"\nRecalled {len(memories)} relevant memories")


async def example_7_predictive_intelligence():
    """Example 7: Predictive intelligence"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Predictive Intelligence")
    print("="*60 + "\n")
    
    cerebro = CerebroCore({"name": "Researcher", "field": "Biotech"})
    await cerebro.start()
    await cerebro.personalize()
    
    # Get predictions
    context = await cerebro.get_full_context()
    predictions = await cerebro.predictor.predict_next_actions(context)
    
    print("Predicted next actions:")
    for i, prediction in enumerate(predictions, 1):
        print(f"  {i}. {prediction}")
    
    # Pre-cache predicted needs
    await cerebro.predictor.pre_cache_likely_needs(predictions)
    print("\n✓ Pre-cached likely needs for faster response")


async def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("CEREBRO USAGE EXAMPLES")
    print("Big dogs eat first - Autonomous Networkologist Copilot")
    print("="*70)
    
    # Run examples
    await example_1_basic_initialization()
    await example_2_query_processing()
    await example_3_nightly_report()
    await example_4_copilot_mode()
    await example_5_cognitive_profiles()
    await example_6_memory_system()
    await example_7_predictive_intelligence()
    
    print("\n" + "="*70)
    print("All examples completed! ✓")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
