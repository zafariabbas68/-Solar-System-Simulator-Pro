#!/usr/bin/env python3
"""
Enhanced realistic solar system visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import plotly.graph_objects as go
from solar_system import SolarSystem
from data.constants import AU
import json


class RealisticSolarSystemVisualizer:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.load_real_orbital_elements()

    def load_real_orbital_elements(self):
        """Load more realistic orbital elements including inclinations"""
        with open('data/planet_data.json', 'r') as f:
            self.planet_data = json.load(f)

    def create_realistic_2d_plot(self):
        """Create 2D plot with realistic elliptical orbits"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        # Plot 1: Inner Solar System (detailed view)
        self._plot_inner_solar_system(ax1)

        # Plot 2: Complete Solar System (scale view)
        self._plot_complete_solar_system(ax2)

        plt.tight_layout()
        return fig, (ax1, ax2)

    def _plot_inner_solar_system(self, ax):
        """Plot inner planets with realistic orbits"""
        ax.set_title('Inner Solar System (Realistic Orbits)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Distance (AU)')
        ax.set_ylabel('Distance (AU)')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')

        inner_planets = ['mercury', 'venus', 'earth', 'mars']

        # Plot sun
        sun_data = self.planet_data['sun']
        ax.scatter(0, 0, color=sun_data['color'], s=200, label='Sun', zorder=10)

        for planet_name in inner_planets:
            planet_data = self.planet_data[planet_name]
            a = planet_data['semi_major_axis'] / AU  # Semi-major axis in AU
            e = planet_data['eccentricity']  # Eccentricity

            # Calculate ellipse parameters
            b = a * np.sqrt(1 - e ** 2)  # Semi-minor axis
            width = 2 * a
            height = 2 * b

            # Create ellipse patch
            ellipse = Ellipse(xy=(0, 0), width=width, height=height,
                              angle=0, fill=False,
                              edgecolor=planet_data['color'],
                              linewidth=2, alpha=0.7,
                              label=f"{planet_data['name']} orbit")
            ax.add_patch(ellipse)

            # Plot current position (simplified - at perihelion)
            current_x = a * (1 - e)
            ax.scatter(current_x, 0, color=planet_data['color'], s=50,
                       label=planet_data['name'], edgecolors='black')

        ax.legend()
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

    def _plot_complete_solar_system(self, ax):
        """Plot complete solar system with logarithmic scale"""
        ax.set_title('Complete Solar System (Logarithmic Scale)', fontsize=14, fontweight='bold')
        ax.set_xlabel('Distance (AU) - Log Scale')
        ax.set_ylabel('Distance (AU) - Log Scale')
        ax.grid(True, alpha=0.3)

        # Plot sun
        sun_data = self.planet_data['sun']
        ax.scatter(1, 1, color=sun_data['color'], s=300, label='Sun', zorder=10)

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                a = planet_data['semi_major_axis'] / AU  # Semi-major axis in AU
                e = planet_data['eccentricity']

                # Use logarithmic scale for better visualization
                log_a = np.log10(a + 1)

                # Plot orbit as circle (simplified for log scale)
                orbit_circle = plt.Circle((log_a, log_a), log_a * 0.1,
                                          fill=False, edgecolor=planet_data['color'],
                                          linewidth=2, alpha=0.6,
                                          label=f"{planet_data['name']} orbit")
                ax.add_patch(orbit_circle)

                # Plot planet position
                ax.scatter(log_a, log_a, color=planet_data['color'], s=100,
                           label=planet_data['name'], edgecolors='black')

        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xlim(0, 2)
        ax.set_ylim(0, 2)

    def create_scale_comparison_plot(self):
        """Create plots showing real scale comparisons"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

        # Plot 1: Real distance scale
        self._plot_real_distance_scale(ax1)

        # Plot 2: Real size scale
        self._plot_real_size_scale(ax2)

        plt.tight_layout()
        return fig

    def _plot_real_distance_scale(self, ax):
        """Plot showing the real scale of solar system distances"""
        distances = []
        planet_names = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                distances.append(planet_data['semi_major_axis'] / AU)
                planet_names.append(planet_data['name'])
                colors.append(planet_data['color'])

        # Create bar plot
        bars = ax.bar(planet_names, distances, color=colors, alpha=0.7)
        ax.set_title('Real Planetary Distances from Sun', fontsize=14, fontweight='bold')
        ax.set_ylabel('Distance (AU)')
        ax.tick_params(axis='x', rotation=45)

        # Add value labels
        for bar, distance in zip(bars, distances):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f'{distance:.1f} AU', ha='center', va='bottom')

    def _plot_real_size_scale(self, ax):
        """Plot showing relative planet sizes"""
        sizes = []
        planet_names = []
        colors = []

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                # Convert radius to kilometers for better scale
                sizes.append(planet_data['radius'] / 1000)  # in km
                planet_names.append(planet_data['name'])
                colors.append(planet_data['color'])

        # Create bar plot
        bars = ax.bar(planet_names, sizes, color=colors, alpha=0.7)
        ax.set_title('Real Planetary Sizes (Radius)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Radius (km)')
        ax.tick_params(axis='x', rotation=45)

        # Add value labels
        for bar, size in zip(bars, sizes):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1000,
                    f'{size:,.0f} km', ha='center', va='bottom', fontsize=8)

    def create_3d_realistic_orbits(self):
        """Create 3D plot with realistic orbital inclinations"""
        fig = go.Figure()

        # Add realistic orbits with inclinations
        inclinations = {
            'mercury': 7.0, 'venus': 3.4, 'earth': 0.0, 'mars': 1.9,
            'jupiter': 1.3, 'saturn': 2.5, 'uranus': 0.8, 'neptune': 1.8
        }

        for planet_name, planet_data in self.planet_data.items():
            if planet_data['type'] == 'planet':
                a = planet_data['semi_major_axis'] / AU
                e = planet_data['eccentricity']
                inclination = np.radians(inclinations.get(planet_name, 0))

                # Generate elliptical orbit points
                theta = np.linspace(0, 2 * np.pi, 100)
                r = a * (1 - e ** 2) / (1 + e * np.cos(theta))

                # Convert to 3D coordinates with inclination
                x = r * np.cos(theta)
                y = r * np.sin(theta) * np.cos(inclination)
                z = r * np.sin(theta) * np.sin(inclination)

                # Add orbit trace
                fig.add_trace(go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color=planet_data['color'], width=3),
                    name=f"{planet_data['name']} Orbit"
                ))

                # Add planet
                fig.add_trace(go.Scatter3d(
                    x=[x[0]], y=[y[0]], z=[z[0]],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=planet_data['color'],
                        line=dict(color='black', width=1)
                    ),
                    name=planet_data['name']
                ))

        # Add sun
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(
                size=15,
                color='#FDB813',
                line=dict(color='black', width=2)
            ),
            name='Sun'
        ))

        fig.update_layout(
            title='3D Solar System with Realistic Orbital Inclinations',
            scene=dict(
                xaxis_title='X (AU)',
                yaxis_title='Y (AU)',
                zaxis_title='Z (AU)',
                aspectmode='data'
            ),
            width=1000,
            height=800
        )

        return fig


def main():
    print("🪐 Creating Realistic Solar System Visualizations...")

    # Create solar system and run simulation
    solar_system = SolarSystem()
    solar_system.simulate(time_span=365, n_steps=500)

    # Create realistic visualizer
    realistic_viz = RealisticSolarSystemVisualizer(solar_system)

    print("1. Creating realistic 2D orbits...")
    fig1, axes = realistic_viz.create_realistic_2d_plot()
    plt.savefig('realistic_orbits_2d.png', dpi=300, bbox_inches='tight')

    print("2. Creating scale comparison plots...")
    fig2 = realistic_viz.create_scale_comparison_plot()
    plt.savefig('realistic_scales.png', dpi=300, bbox_inches='tight')

    print("3. Creating 3D realistic orbits...")
    fig3 = realistic_viz.create_3d_realistic_orbits()
    fig3.write_html('realistic_3d_orbits.html')

    print("4. Creating enhanced comparison...")
    # Show the difference between simplified and realistic
    from visualization import SolarSystemVisualizer
    simple_viz = SolarSystemVisualizer(solar_system)
    fig_simple, ax_simple = simple_viz.create_static_plot()
    plt.savefig('comparison_simple_vs_realistic.png', dpi=300, bbox_inches='tight')

    print("\n🎉 Realistic visualizations created!")
    print("📁 New files:")
    print("   - realistic_orbits_2d.png (elliptical orbits)")
    print("   - realistic_scales.png (distance & size scales)")
    print("   - realistic_3d_orbits.html (3D with inclinations)")
    print("   - comparison_simple_vs_realistic.png")

    plt.show()


if __name__ == "__main__":
    main()