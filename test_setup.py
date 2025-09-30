#!/usr/bin/env python3
"""
Test script to verify the solar system simulator setup
"""

try:
    import numpy as np
    import matplotlib.pyplot as plt
    import json
    print("✓ Basic imports successful")
    
    # Test data loading
    with open('data/planet_data.json', 'r') as f:
        planet_data = json.load(f)
    print(f"✓ Loaded data for {len(planet_data)} celestial bodies")
    
    # Test constants
    from data.constants import AU, G, SOLAR_MASS
    print(f"✓ Constants loaded: AU={AU}, G={G:.2e}")
    
    # Test solar system class
    from solar_system import SolarSystem
    ss = SolarSystem()
    print(f"✓ SolarSystem initialized with {len(ss.bodies)} bodies")
    
    print("\n🎉 All tests passed! You're ready to run the simulator.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check the error above and let me know.")
