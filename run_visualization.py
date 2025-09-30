#!/usr/bin/env python3
"""
Simple script to run solar system visualizations
"""

import matplotlib.pyplot as plt
from solar_system import SolarSystem
from visualization import SolarSystemVisualizer
from statistics import SolarSystemStatistics

def main():
    print("🚀 Initializing Solar System Simulator...")
    
    # Create solar system
    solar_system = SolarSystem()
    print(f"✅ Loaded {len(solar_system.bodies)} celestial bodies")
    
    # Run simulation
    print("🔄 Running simulation...")
    solar_system.simulate(time_span=365 * 2, n_steps=1000)  # 2 years
    
    # Create visualizer
    visualizer = SolarSystemVisualizer(solar_system)
    
    print("\n📊 Creating visualizations...")
    
    # 1. Create static solar system plot
    print("1. Creating static solar system plot...")
    fig1, ax1 = visualizer.create_static_plot()
    plt.savefig('solar_system.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved as 'solar_system.png'")
    
    # 2. Create comparison plots
    print("2. Creating planetary comparison plots...")
    fig2 = visualizer.create_comparison_plots()
    plt.savefig('planetary_comparison.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved as 'planetary_comparison.png'")
    
    # 3. Create 3D plot
    print("3. Creating 3D interactive visualization...")
    fig3 = visualizer.create_3d_plotly_visualization()
    fig3.write_html('solar_system_3d.html')
    print("   ✅ Saved as 'solar_system_3d.html'")
    
    # 4. Create statistics
    print("4. Generating statistics...")
    stats = SolarSystemStatistics(solar_system)
    
    # Kepler's law verification
    stats.keplers_law_verification()
    plt.savefig('keplers_law.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved as 'keplers_law.png'")
    
    # Orbital energy analysis
    stats.orbital_energy_analysis()
    plt.savefig('orbital_energy.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved as 'orbital_energy.png'")
    
    # Correlation analysis
    stats.correlation_analysis()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    print("   ✅ Saved as 'correlation_matrix.png'")
    
    print("\n🎉 All visualizations created successfully!")
    print("\n📁 Generated files:")
    print("   - solar_system.png (2D solar system view)")
    print("   - planetary_comparison.png (comparison charts)")
    print("   - solar_system_3d.html (interactive 3D plot)")
    print("   - keplers_law.png (Kepler's law verification)")
    print("   - orbital_energy.png (energy analysis)")
    print("   - correlation_matrix.png (property correlations)")
    
    print("\n🖥️ Opening visualizations...")
    plt.show()

if __name__ == "__main__":
    main()
